from typing import Any


class Permissions(object):
    type: list[str] = []
    nivel1: list[str] = []
    nivel2: list[str] = []
    nivel3: list[str] = []
    nivel4: list[str] = []
    nivel5: list[str] = []
    nivel6: list[str] = []

    def load(self, session: dict[str, Any]) -> None:
        permissions: dict[str, list[str]] = session.get("permissions", {})
        self.type = permissions.get("type", [])
        self.nivel1 = permissions.get("nivel1", [])
        self.nivel2 = permissions.get("nivel2", [])
        self.nivel3 = permissions.get("nivel3", [])
        self.nivel4 = permissions.get("nivel4", [])
        self.nivel5 = permissions.get("nivel5", [])
        self.nivel6 = permissions.get("nivel6", [])

    def update(self, result_permissions) -> None:
        self.type = []
        self.nivel1 = []
        self.nivel2 = []
        self.nivel3 = []
        self.nivel4 = []
        self.nivel5 = []
        self.nivel6 = []

        permissions: dict[str, list[str]]
        permissions = {
            "type": [],
        }

        for x in result_permissions:
            model_permission = x

            permission: str = model_permission.permission
            desmembered: list[str] = permission.split(":")
            nivels: list[str] = desmembered[0].split("_")

            if permission not in permissions["type"]:
                permissions["type"].append(permission)
                self_nivel = getattr(self, "type")
                self_nivel.append(permission)
                setattr(self, "type", self_nivel)

            permission_nivel: str = ""
            for x, y in enumerate(nivels):
                x = x + 1

                nivel: str = f"nivel{str(x)}"
                if nivel not in list(permissions.keys()):
                    permissions.update({nivel: []})

                if x > 1:
                    permission_nivel += "_"

                permission_nivel += y

                if permission_nivel not in permissions[nivel]:
                    permissions[nivel].append(permission_nivel)

                    self_nivel = getattr(self, nivel)
                    self_nivel.append(permission_nivel)
                    setattr(self, nivel, self_nivel)

    def get(self) -> dict[str, list[str]]:
        return {
            "type": self.type,
            "nivel1": self.nivel1,
            "nivel2": self.nivel2,
            "nivel3": self.nivel3,
            "nivel4": self.nivel4,
            "nivel5": self.nivel5,
            "nivel6": self.nivel6,
        }
