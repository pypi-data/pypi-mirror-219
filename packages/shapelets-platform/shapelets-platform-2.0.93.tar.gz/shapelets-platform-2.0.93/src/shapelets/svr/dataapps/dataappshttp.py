import json
import os
from decimal import Decimal

from blacksheep import FromJSON, Request, unauthorized, WebSocket
from blacksheep.server.controllers import ApiController, delete, file, get, post, ws
from guardpost.authentication import Identity
from requests import Session
from typing import List, Optional

from .dataapps_ws import DataAppChangeListeners
from .idataappsservice import IDataAppsService

from ..groups import InvalidGroupName
from ..model import SignedPrincipalId
from ..model.dataapps import DataAppAttributes, DataAppProfile
from ..users import UserDoesNotBelong, WritePermission


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class DataAppsHttpServer(ApiController):
    def __init__(self, svr: IDataAppsService) -> None:
        self._svr = svr
        super().__init__()
        self.dataapp_change_listeners = DataAppChangeListeners()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/dataapps'

    @ws("/ws")
    async def ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            msg = await websocket.receive_text()
            self.dataapp_change_listeners.add(msg, websocket)
            while True:
                msg = await websocket.receive_text()
        except Exception as e:
            print(e)
        finally:
            self.dataapp_change_listeners.remove(websocket)

    @get("/")
    async def dataapp_list(self, user: Identity) -> List[DataAppProfile]:
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        user_id = user.claims["userId"]
        return self._svr.get_all(user_id)

    @get("/user")
    async def user_local_dataapp_list(self, user: Identity) -> List[DataAppAttributes]:
        """
        Returns all dataApps that belong only to the user. Like the user local develop section.
        """
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        user_id = user.claims["userId"]
        return self._svr.user_local_dataapp_list(user_id)

    @get("/groups")
    async def user_group_dataapp_list(self, user: Identity) -> List[DataAppAttributes]:
        """
        Returns all dataApps that belong to any group that the user belongs.
        """
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        user_id = user.claims["userId"]
        return self._svr.user_group_dataapp_list(user_id)

    @post("/")
    async def create(self, request: Request, attributes: FromJSON[DataAppAttributes], data) -> DataAppProfile:
        try:
            if request.identity:
                user_id = request.identity.claims["userId"]
            elif request.get_first_header(b"authorization"):
                header_value = request.get_first_header(b"authorization")
                token = header_value.decode('ascii').split("Bearer ", 1)[1]
                principal = SignedPrincipalId.from_token(token)
                if principal is None:
                    raise RuntimeError(f"Invalid bearer token: {header_value}")
                user_id = principal.userId
            else:
                message = "Unable to find user for dataApp registration. Please, login."
                print(message)
                return unauthorized(message)
            dataapp_attributes = DataAppAttributes(name=attributes.value.name,
                                                   major=attributes.value.major,
                                                   minor=attributes.value.minor,
                                                   description=attributes.value.description,
                                                   specId=attributes.value.specId,
                                                   tags=attributes.value.tags,
                                                   groups=attributes.value.groups,
                                                   userId=user_id)
            data_app = self._svr.create(dataapp_attributes, data)
            await self.dataapp_change_listeners.notify(data_app.name, data_app.major, data_app.minor, False)
            return data_app
        except UserDoesNotBelong as e:
            return self.bad_request(str(e))
        except InvalidGroupName as e:
            return self.bad_request(str(e))
        except WritePermission as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/{id}")
    async def get_dataapp(self, dataAppName: str) -> DataAppAttributes:
        return self._svr.get_dataapp(dataAppName)

    @delete("/")
    async def delete_all(self) -> bool:
        return self._svr.delete_all()

    @delete("/{id}")
    async def delete(self, uid: int, user: Identity) -> bool:
        if user is None:
            raise RuntimeError(f"Unable to find user. Please, login.")
        user_id = user.claims["userId"]
        dataapp = self._svr.get_dataapp_by_id(uid)
        if self._svr.delete_dataapp(uid, user_id):
            await self.dataapp_change_listeners.notify(dataapp.name, dataapp.major, dataapp.minor, False)
            return self.ok("DataApp removed successfully.")
        return self.bad_request()

    @get("/{id}/privileges")
    async def get_dataapp_privileges(self, dataapp_id: int) -> List[DataAppAttributes]:
        return self._svr.get_dataapp_privileges(dataapp_id)

    @get("/{id}/versions")
    async def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return json.dumps(self._svr.get_dataapp_versions(dataAppName), cls=DecimalEncoder)

    @get("spec/{specId}")
    async def get_dataapp_spec(self, specId: str) -> file:
        shapelets_dir = os.path.expanduser('~/.shapelets')
        data_apps_store = os.path.join(shapelets_dir, 'dataAppsStore')
        spec_path = os.path.join(data_apps_store, f"{specId}.json")
        return file(spec_path, "multipart/form-data")

    @get("/{id}/{major}/{minor}")
    async def get_dataapp_by_version(self, dataAppName: str, major: int, minor: int) -> DataAppProfile:
        return self._svr.get_dataapp_by_version(dataAppName, major, minor)

    @get("/{id}/lastVersion")
    async def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self._svr.get_dataapp_last_version(dataAppName)

    @get("/{id}/tags")
    async def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self._svr.get_dataapp_tags(dataAppName)


class DataAppsHttpProxy(IDataAppsService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/')

    def user_local_dataapp_list(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/user')

    def user_group_dataapp_list(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/groups')

    def create(self, dataapp) -> DataAppProfile:
        payload = DataAppAttributes(name=dataapp.name,
                                    major=dataapp.version[0] if dataapp.version else None,
                                    minor=dataapp.version[1] if dataapp.version else None,
                                    description=dataapp.description,
                                    specId=dataapp.to_json(),
                                    tags=dataapp.tags,
                                    groups=dataapp.groups)
        params = None
        if dataapp._data:
            params = [("data", dataapp._data)]
        response = self.session.post('/api/dataapps/', json=json.loads(payload.json()), params=params)
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response

    def get_dataapp(self, dataAppName: str) -> DataAppAttributes:
        return self.session.get('/api/dataapps/', params=[("dataAppName", dataAppName)])

    def delete_dataapp(self, uid: int):
        self.session.delete('/api/dataapps/{id}', params=[("uid", uid)])

    def delete_all(self) -> bool:
        self.session.delete('/api/dataapps/')
        return True

    def get_dataapp_privileges(self, dataAppName: str) -> List[DataAppAttributes]:
        pass

    def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return self.session.get('/api/{id}/versions', params=[("dataAppName", dataAppName)])

    def get_dataapp_by_id(self, uid: int) -> DataAppProfile:
        return self.session.get('/api/{id}', params=[("uid", uid)])

    def get_dataapp_by_version(self, dataAppName: str, major: int, minor: int) -> DataAppProfile:
        response = self.session.get(f'/api/dataapps/{id}/{major}/{minor}', params=[("dataAppName", dataAppName),
                                                                                   ("major", major),
                                                                                   ("minor", minor)])
        return response.json()

    def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self.session.get('/api/{id}/lastVersion', params=[("dataAppName", dataAppName)])

    def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self.session.get('/api/{id}/tags', params=[("dataAppName", dataAppName)])
