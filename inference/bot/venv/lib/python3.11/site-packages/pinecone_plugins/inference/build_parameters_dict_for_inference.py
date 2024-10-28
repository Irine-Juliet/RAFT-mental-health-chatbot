from .core.client.model.embed_request_parameters import EmbedRequestParameters


def build_parameters_dict_for_inference(params: dict):
    """
    Build a dictionary of parameters for inference.

    :param params: A dictionary of parameters.
    :type params: dict, required
    """
    if not params.get("input_type") is None and not params.get("truncate") is None:
        return EmbedRequestParameters(
            input_type=params.get("input_type"), truncate=params.get("truncate")
        )

    if not params.get("input_type") is None and params.get("truncate") is None:
        return EmbedRequestParameters(input_type=params.get("input_type"))

    if not params.get("truncate") is None and params.get("input_type") is None:
        return EmbedRequestParameters(truncate=params.get("truncate"))
