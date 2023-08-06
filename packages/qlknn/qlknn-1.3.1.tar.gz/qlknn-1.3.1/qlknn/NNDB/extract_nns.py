from IPython import embed

# import mega_nn
import gc
import numpy as np
import pandas as pd
from model import Network, NetworkJSON
from peewee import Param
import os
import sys

networks_path = os.path.abspath(os.path.join((os.path.abspath(__file__)), "../../networks"))
sys.path.append(networks_path)
from run_model import QuaLiKizNDNN

store = pd.HDFStore("./7D_nions0_flat.h5")
features = 7
input = store["megarun1/input"]
df = store["megarun1/flattened"]

# nn = mega_nn.nn

root_name = "/megarun1/nndb_nn/"
query = Network.select(Network.target_names).distinct().tuples()
for query_res in query:
    (target_names,) = query_res

    if len(target_names) == 1:
        target_name = target_names[0]
    else:
        NotImplementedError("Multiple targets not implemented yet")
    print(target_name)
    parent_name = root_name + target_name + "/"
    subquery = (
        Network.select(Network.id, NetworkJSON.network_json)
        .where(Network.target_names == Param(target_names))
        .join(NetworkJSON)
        .tuples()
    )
    for subquery_res in subquery:
        id, json_dict = subquery_res

        nn = QuaLiKizNDNN(json_dict)
        network_name = parent_name + str(id)

        if len(nn.feature_names) != features:
            print(
                "Skipping",
                id,
                ": has",
                len(nn.feature_names),
                "features instead of",
                features,
            )
            continue

        if network_name in store:
            pass

        else:
            print("Generating ", network_name)
            df_nn = nn.get_output(**input, clip_low=True, clip_high=True)
            df_nn.index = input.index
            store[network_name] = df_nn
            del df_nn
            gc.collect()

        network_name = parent_name + str(id) + "_noclip"
        if network_name in store:
            pass
        else:
            print("Generating ", network_name)
            df_nn = nn.get_output(**input, clip_low=False, clip_high=False)
            df_nn.index = input.index
            store[network_name] = df_nn
            del df_nn
            gc.collect()
embed()
# df_nn = nn.get_outputs(**input)
# df_nn.index = input.index
# store[] = df_nn
