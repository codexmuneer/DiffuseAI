# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

# import text2img_pb2 as text2img__pb2
from proto_files import text2img_pb2 as text2img__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in text2img_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TextToImageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Generate = channel.unary_stream(
                '/text2img.TextToImage/Generate',
                request_serializer=text2img__pb2.GenerationRequest.SerializeToString,
                response_deserializer=text2img__pb2.GenerationResponse.FromString,
                _registered_method=True)
        self.EnhancePrompt = channel.unary_unary(
                '/text2img.TextToImage/EnhancePrompt',
                request_serializer=text2img__pb2.PromptEnhancementRequest.SerializeToString,
                response_deserializer=text2img__pb2.PromptEnhancementResponse.FromString,
                _registered_method=True)
        self.ApplyFilter = channel.unary_unary(
                '/text2img.TextToImage/ApplyFilter',
                request_serializer=text2img__pb2.ImageFilterRequest.SerializeToString,
                response_deserializer=text2img__pb2.ImageFilterResponse.FromString,
                _registered_method=True)
        self.GenerateCaption = channel.unary_unary(
                '/text2img.TextToImage/GenerateCaption',
                request_serializer=text2img__pb2.CaptionGenerationRequest.SerializeToString,
                response_deserializer=text2img__pb2.CaptionGenerationResponse.FromString,
                _registered_method=True)


class TextToImageServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Generate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EnhancePrompt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplyFilter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GenerateCaption(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TextToImageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Generate': grpc.unary_stream_rpc_method_handler(
                    servicer.Generate,
                    request_deserializer=text2img__pb2.GenerationRequest.FromString,
                    response_serializer=text2img__pb2.GenerationResponse.SerializeToString,
            ),
            'EnhancePrompt': grpc.unary_unary_rpc_method_handler(
                    servicer.EnhancePrompt,
                    request_deserializer=text2img__pb2.PromptEnhancementRequest.FromString,
                    response_serializer=text2img__pb2.PromptEnhancementResponse.SerializeToString,
            ),
            'ApplyFilter': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyFilter,
                    request_deserializer=text2img__pb2.ImageFilterRequest.FromString,
                    response_serializer=text2img__pb2.ImageFilterResponse.SerializeToString,
            ),
            'GenerateCaption': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateCaption,
                    request_deserializer=text2img__pb2.CaptionGenerationRequest.FromString,
                    response_serializer=text2img__pb2.CaptionGenerationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'text2img.TextToImage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('text2img.TextToImage', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TextToImage(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Generate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/text2img.TextToImage/Generate',
            text2img__pb2.GenerationRequest.SerializeToString,
            text2img__pb2.GenerationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EnhancePrompt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/text2img.TextToImage/EnhancePrompt',
            text2img__pb2.PromptEnhancementRequest.SerializeToString,
            text2img__pb2.PromptEnhancementResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ApplyFilter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/text2img.TextToImage/ApplyFilter',
            text2img__pb2.ImageFilterRequest.SerializeToString,
            text2img__pb2.ImageFilterResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GenerateCaption(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/text2img.TextToImage/GenerateCaption',
            text2img__pb2.CaptionGenerationRequest.SerializeToString,
            text2img__pb2.CaptionGenerationResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
