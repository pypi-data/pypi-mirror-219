from typing import Any
from typing import Dict


async def get_appended_prefix(
    hub,
    ctx,
    data: dict = None,
) -> Dict[str, Any]:
    if data:
        for k, v in data.items():
            if ("_ref" in k and isinstance(v, str)) and (
                ("name=" not in v) and ("/api" not in v)
            ):
                obj_prefix = k.split("_ref")[0]
                new_value = await hub.tool.nsx_alb.session.append_prefix(
                    ctx, obj_prefix=obj_prefix, value=v
                )
                data.update({k: new_value})
    return data
