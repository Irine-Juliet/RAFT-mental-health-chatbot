from .repl_overrides import install_repl_overrides
from .inference import Inference
from .build_parameters_dict_for_inference import build_parameters_dict_for_inference
from pinecone_plugin_interface import PluginMetadata

install_repl_overrides()

__installables__ = [
    PluginMetadata(
        target_object="Pinecone", namespace="inference", implementation_class=Inference
    ),
    PluginMetadata(
        target_object="PineconeGRPC",
        namespace="inference",
        implementation_class=Inference,
    ),
]
