import oci
from datetime import datetime
import time
import sys

v1 = sys.argv[1]

def instances(p_signer,p_compid):
    Instances   = oci.core.ComputeClient(config={},signer=p_signer)
    inst_tag = {}
    for instance in Instances.list_instances(compartment_id=p_compid).data:
        if instance.lifecycle_state in ['RUNNING','STOPPED']:
            try:
                inst_tag[instance.id] = {}
                inst_tag[instance.id]['schedule'] = instance.freeform_tags["myschedule"]
                inst_tag[instance.id]['lifecycle_state'] = instance.lifecycle_state
            except Exception as e:
                inst_tag.pop(instance.id)
    return inst_tag

def instance_action(p_signer,p_ocid,p_action):
    Instances   = oci.core.ComputeClient(config={},signer=p_signer)
    try:
        result = Instances.instance_action(p_ocid,p_action)
    except  Exception as e:
        result = e.args[-1]
    return result    

if __name__ == "__main__":
    signer = oci.auth.signers.get_resource_principals_signer()
    while True:
        ret  = instances(signer,v1)
        hh = int(datetime.now().strftime("%H"))
        print('++++++++++++++++++++++++++++++++++++++++++++++')
        print(ret)
        for i in ret.keys():
            print(f'*****************************************')
            print(f'Instance: {i}')
            if ret[i]:
                print(f'schedule exists: {ret[i]["schedule"].split(",")}')
                print(f'schedule for {hh} is {ret[i]["schedule"].split(",")[hh]}')
                print(f'Instance state is {ret[i]["lifecycle_state"]}')
                if ret[i]["schedule"].split(',')[hh]  == "s"  and ret[i]["lifecycle_state"] == "RUNNING":
                    print(f'Time to stop the instance...')
                    res_action = instance_action(signer,i,"STOP")
                elif ret[i]["schedule"].split(',')[hh]  == "r"  and ret[i]["lifecycle_state"] == "STOPPED":
                    print(f'Time to start the instance...')
                    res_action = instance_action(signer,i,"START")
                else:
                    print(f'Leave it...')
            else:
                print(f'No schedule...')
        time.sleep(100)     


