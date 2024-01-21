from typing import Dict, List, Union

from fastapi import Depends, HTTPException

from app import app, xray
from app.db import Session, crud, get_db
from app.models.admin import Admin
from app.models.proxy import InboundHost, Inbound, ProxyTypes, InboundBase
from app.models.system import SystemStats
from app.models.user import UserStatus
from app.utils.system import memory_usage, cpu_usage, realtime_bandwidth
from app import __version__


@app.get("/api/system", tags=["System"], response_model=SystemStats)
def get_system_stats(db: Session = Depends(get_db), admin: Admin = Depends(Admin.get_current)):
    mem = memory_usage()
    cpu = cpu_usage()
    system = crud.get_system_usage(db)
    dbadmin: Union[Admin, None] = crud.get_admin(db, admin.username)

    total_user = crud.get_users_count(db, admin=dbadmin if not admin.is_sudo else None)
    users_active = crud.get_users_count(db, status=UserStatus.active, admin=dbadmin if not admin.is_sudo else None)
    realtime_bandwidth_stats = realtime_bandwidth()

    return SystemStats(
        version=__version__,
        mem_total=mem.total,
        mem_used=mem.used,
        cpu_cores=cpu.cores,
        cpu_usage=cpu.percent,
        total_user=total_user,
        users_active=users_active,
        incoming_bandwidth=system.uplink,
        outgoing_bandwidth=system.downlink,
        incoming_bandwidth_speed=realtime_bandwidth_stats.incoming_bytes,
        outgoing_bandwidth_speed=realtime_bandwidth_stats.outgoing_bytes,
    )


@app.get('/api/inbounds', tags=["System"], response_model=Dict[str, List[Inbound]])
def get_inbounds(db: Session = Depends(get_db), admin: Admin = Depends(Admin.get_current)):
    inbounds = crud.get_all_inbounds(db)# xray.config.inbounds_by_protocol
    resp = {}
    for i in inbounds:
        if resp.get(i.protocol):
            resp[i.protocol].append(i)
        else:
            resp[i.protocol] = [i]
    return resp


@app.get('/api/hosts', tags=["System"], response_model=Dict[str, List[InboundHost]])
def get_hosts(db: Session = Depends(get_db), admin: Admin = Depends(Admin.get_current)):
    if not admin.is_sudo:
        raise HTTPException(status_code=403, detail="You're not allowed")

    # hosts = {}
    hosts = crud.get_all_hosts(db)
    #for inbound_tag in xray.config.inbounds_by_tag:
    #    hosts[inbound_tag] = crud.get_hosts(db, inbound_tag)

    return hosts


@app.put('/api/hosts', tags=["System"], response_model=Dict[str, List[InboundHost]])
def modify_hosts(modified_hosts: Dict[str, List[InboundHost]],
                 db: Session = Depends(get_db),
                 admin: Admin = Depends(Admin.get_current)):
    if not admin.is_sudo:
        raise HTTPException(status_code=403, detail="You're not allowed")

    # validate
    #for inbound_id, hosts in modified_hosts.items():
    #    if not xray.config.inbounds_by_id.get(inbound_id):
    #        raise HTTPException(status_code=400, detail=f"Inbound {inbound_id} doesn't exist")

    for inbound_id, hosts in modified_hosts.items():
        crud.update_hosts(db, inbound_id, hosts)

    #xray.hosts.update()

    hosts = {}
    #for inbound_tag in xray.config.inbounds_by_tag:
    #    hosts[inbound_tag] = crud.get_hosts(db, inbound_tag)

    return hosts