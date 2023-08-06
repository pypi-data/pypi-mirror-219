# -*- coding: utf-8 -*-

"""
verizon

This file was automatically generated by APIMATIC v3.0 (
 https://www.apimatic.io ).
"""


class HttpStatusCodeEnum(object):

    """Implementation of the 'HttpStatusCode' enum.

    HTML error code and description.

    Attributes:
        ENUM_100 CONTINUE: TODO: type description here.
        ENUM_101 SWITCHING_PROTOCOLS: TODO: type description here.
        ENUM_102 PROCESSING: TODO: type description here.
        ENUM_103 CHECKPOINT: TODO: type description here.
        ENUM_200 OK: TODO: type description here.
        ENUM_201 CREATED: TODO: type description here.
        ENUM_202 ACCEPTED: TODO: type description here.
        ENUM_203 NON_AUTHORITATIVE_INFORMATION: TODO: type description here.
        ENUM_204 NO_CONTENT: TODO: type description here.
        ENUM_205 RESET_CONTENT: TODO: type description here.
        ENUM_206 PARTIAL_CONTENT: TODO: type description here.
        ENUM_207 MULTI_STATUS: TODO: type description here.
        ENUM_208 ALREADY_REPORTED: TODO: type description here.
        ENUM_226 IM_USED: TODO: type description here.
        ENUM_300 MULTIPLE_CHOICES: TODO: type description here.
        ENUM_301 MOVED_PERMANENTLY: TODO: type description here.
        ENUM_302 FOUND: TODO: type description here.
        ENUM_302 MOVED_TEMPORARILY: TODO: type description here.
        ENUM_303 SEE_OTHER: TODO: type description here.
        ENUM_304 NOT_MODIFIED: TODO: type description here.
        ENUM_305 USE_PROXY: TODO: type description here.
        ENUM_307 TEMPORARY_REDIRECT: TODO: type description here.
        ENUM_308 PERMANENT_REDIRECT: TODO: type description here.
        ENUM_400 BAD_REQUEST: TODO: type description here.
        ENUM_401 UNAUTHORIZED: TODO: type description here.
        ENUM_402 PAYMENT_REQUIRED: TODO: type description here.
        ENUM_403 FORBIDDEN: TODO: type description here.
        ENUM_404 NOT_FOUND: TODO: type description here.
        ENUM_405 METHOD_NOT_ALLOWED: TODO: type description here.
        ENUM_406 NOT_ACCEPTABLE: TODO: type description here.
        ENUM_407 PROXY_AUTHENTICATION_REQUIRED: TODO: type description here.
        ENUM_408 REQUEST_TIMEOUT: TODO: type description here.
        ENUM_409 CONFLICT: TODO: type description here.
        ENUM_410 GONE: TODO: type description here.
        ENUM_411 LENGTH_REQUIRED: TODO: type description here.
        ENUM_412 PRECONDITION_FAILED: TODO: type description here.
        ENUM_413 PAYLOAD_TOO_LARGE: TODO: type description here.
        ENUM_413 REQUEST_ENTITY_TOO_LARGE: TODO: type description here.
        ENUM_414 URI_TOO_LONG: TODO: type description here.
        ENUM_414 REQUEST_URI_TOO_LONG: TODO: type description here.
        ENUM_415 UNSUPPORTED_MEDIA_TYPE: TODO: type description here.
        ENUM_416 REQUESTED_RANGE_NOT_SATISFIABLE: TODO: type description
            here.
        ENUM_417 EXPECTATION_FAILED: TODO: type description here.
        ENUM_418 I_AM_A_TEAPOT: TODO: type description here.
        ENUM_419 INSUFFICIENT_SPACE_ON_RESOURCE: TODO: type description here.
        ENUM_420 METHOD_FAILURE: TODO: type description here.
        ENUM_421 DESTINATION_LOCKED: TODO: type description here.
        ENUM_422 UNPROCESSABLE_ENTITY: TODO: type description here.
        ENUM_423 LOCKED: TODO: type description here.
        ENUM_424 FAILED_DEPENDENCY: TODO: type description here.
        ENUM_425 TOO_EARLY: TODO: type description here.
        ENUM_426 UPGRADE_REQUIRED: TODO: type description here.
        ENUM_428 PRECONDITION_REQUIRED: TODO: type description here.
        ENUM_429 TOO_MANY_REQUESTS: TODO: type description here.
        ENUM_431 REQUEST_HEADER_FIELDS_TOO_LARGE: TODO: type description
            here.
        ENUM_451 UNAVAILABLE_FOR_LEGAL_REASONS: TODO: type description here.
        ENUM_500 INTERNAL_SERVER_ERROR: TODO: type description here.
        ENUM_501 NOT_IMPLEMENTED: TODO: type description here.
        ENUM_502 BAD_GATEWAY: TODO: type description here.
        ENUM_503 SERVICE_UNAVAILABLE: TODO: type description here.
        ENUM_504 GATEWAY_TIMEOUT: TODO: type description here.
        ENUM_505 HTTP_VERSION_NOT_SUPPORTED: TODO: type description here.
        ENUM_506 VARIANT_ALSO_NEGOTIATES: TODO: type description here.
        ENUM_507 INSUFFICIENT_STORAGE: TODO: type description here.
        ENUM_508 LOOP_DETECTED: TODO: type description here.
        ENUM_509 BANDWIDTH_LIMIT_EXCEEDED: TODO: type description here.
        ENUM_510 NOT_EXTENDED: TODO: type description here.
        ENUM_511 NETWORK_AUTHENTICATION_REQUIRED: TODO: type description
            here.

    """

    ENUM_100_CONTINUE = '100 CONTINUE'

    ENUM_101_SWITCHING_PROTOCOLS = '101 SWITCHING_PROTOCOLS'

    ENUM_102_PROCESSING = '102 PROCESSING'

    ENUM_103_CHECKPOINT = '103 CHECKPOINT'

    ENUM_200_OK = '200 OK'

    ENUM_201_CREATED = '201 CREATED'

    ENUM_202_ACCEPTED = '202 ACCEPTED'

    ENUM_203_NON_AUTHORITATIVE_INFORMATION = '203 NON_AUTHORITATIVE_INFORMATION'

    ENUM_204_NO_CONTENT = '204 NO_CONTENT'

    ENUM_205_RESET_CONTENT = '205 RESET_CONTENT'

    ENUM_206_PARTIAL_CONTENT = '206 PARTIAL_CONTENT'

    ENUM_207_MULTI_STATUS = '207 MULTI_STATUS'

    ENUM_208_ALREADY_REPORTED = '208 ALREADY_REPORTED'

    ENUM_226_IM_USED = '226 IM_USED'

    ENUM_300_MULTIPLE_CHOICES = '300 MULTIPLE_CHOICES'

    ENUM_301_MOVED_PERMANENTLY = '301 MOVED_PERMANENTLY'

    ENUM_302_FOUND = '302 FOUND'

    ENUM_302_MOVED_TEMPORARILY = '302 MOVED_TEMPORARILY'

    ENUM_303_SEE_OTHER = '303 SEE_OTHER'

    ENUM_304_NOT_MODIFIED = '304 NOT_MODIFIED'

    ENUM_305_USE_PROXY = '305 USE_PROXY'

    ENUM_307_TEMPORARY_REDIRECT = '307 TEMPORARY_REDIRECT'

    ENUM_308_PERMANENT_REDIRECT = '308 PERMANENT_REDIRECT'

    ENUM_400_BAD_REQUEST = '400 BAD_REQUEST'

    ENUM_401_UNAUTHORIZED = '401 UNAUTHORIZED'

    ENUM_402_PAYMENT_REQUIRED = '402 PAYMENT_REQUIRED'

    ENUM_403_FORBIDDEN = '403 FORBIDDEN'

    ENUM_404_NOT_FOUND = '404 NOT_FOUND'

    ENUM_405_METHOD_NOT_ALLOWED = '405 METHOD_NOT_ALLOWED'

    ENUM_406_NOT_ACCEPTABLE = '406 NOT_ACCEPTABLE'

    ENUM_407_PROXY_AUTHENTICATION_REQUIRED = '407 PROXY_AUTHENTICATION_REQUIRED'

    ENUM_408_REQUEST_TIMEOUT = '408 REQUEST_TIMEOUT'

    ENUM_409_CONFLICT = '409 CONFLICT'

    ENUM_410_GONE = '410 GONE'

    ENUM_411_LENGTH_REQUIRED = '411 LENGTH_REQUIRED'

    ENUM_412_PRECONDITION_FAILED = '412 PRECONDITION_FAILED'

    ENUM_413_PAYLOAD_TOO_LARGE = '413 PAYLOAD_TOO_LARGE'

    ENUM_413_REQUEST_ENTITY_TOO_LARGE = '413 REQUEST_ENTITY_TOO_LARGE'

    ENUM_414_URI_TOO_LONG = '414 URI_TOO_LONG'

    ENUM_414_REQUEST_URI_TOO_LONG = '414 REQUEST_URI_TOO_LONG'

    ENUM_415_UNSUPPORTED_MEDIA_TYPE = '415 UNSUPPORTED_MEDIA_TYPE'

    ENUM_416_REQUESTED_RANGE_NOT_SATISFIABLE = '416 REQUESTED_RANGE_NOT_SATISFIABLE'

    ENUM_417_EXPECTATION_FAILED = '417 EXPECTATION_FAILED'

    ENUM_418_I_AM_A_TEAPOT = '418 I_AM_A_TEAPOT'

    ENUM_419_INSUFFICIENT_SPACE_ON_RESOURCE = '419 INSUFFICIENT_SPACE_ON_RESOURCE'

    ENUM_420_METHOD_FAILURE = '420 METHOD_FAILURE'

    ENUM_421_DESTINATION_LOCKED = '421 DESTINATION_LOCKED'

    ENUM_422_UNPROCESSABLE_ENTITY = '422 UNPROCESSABLE_ENTITY'

    ENUM_423_LOCKED = '423 LOCKED'

    ENUM_424_FAILED_DEPENDENCY = '424 FAILED_DEPENDENCY'

    ENUM_425_TOO_EARLY = '425 TOO_EARLY'

    ENUM_426_UPGRADE_REQUIRED = '426 UPGRADE_REQUIRED'

    ENUM_428_PRECONDITION_REQUIRED = '428 PRECONDITION_REQUIRED'

    ENUM_429_TOO_MANY_REQUESTS = '429 TOO_MANY_REQUESTS'

    ENUM_431_REQUEST_HEADER_FIELDS_TOO_LARGE = '431 REQUEST_HEADER_FIELDS_TOO_LARGE'

    ENUM_451_UNAVAILABLE_FOR_LEGAL_REASONS = '451 UNAVAILABLE_FOR_LEGAL_REASONS'

    ENUM_500_INTERNAL_SERVER_ERROR = '500 INTERNAL_SERVER_ERROR'

    ENUM_501_NOT_IMPLEMENTED = '501 NOT_IMPLEMENTED'

    ENUM_502_BAD_GATEWAY = '502 BAD_GATEWAY'

    ENUM_503_SERVICE_UNAVAILABLE = '503 SERVICE_UNAVAILABLE'

    ENUM_504_GATEWAY_TIMEOUT = '504 GATEWAY_TIMEOUT'

    ENUM_505_HTTP_VERSION_NOT_SUPPORTED = '505 HTTP_VERSION_NOT_SUPPORTED'

    ENUM_506_VARIANT_ALSO_NEGOTIATES = '506 VARIANT_ALSO_NEGOTIATES'

    ENUM_507_INSUFFICIENT_STORAGE = '507 INSUFFICIENT_STORAGE'

    ENUM_508_LOOP_DETECTED = '508 LOOP_DETECTED'

    ENUM_509_BANDWIDTH_LIMIT_EXCEEDED = '509 BANDWIDTH_LIMIT_EXCEEDED'

    ENUM_510_NOT_EXTENDED = '510 NOT_EXTENDED'

    ENUM_511_NETWORK_AUTHENTICATION_REQUIRED = '511 NETWORK_AUTHENTICATION_REQUIRED'
