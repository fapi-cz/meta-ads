from contextlib import ExitStack
from ctypes import CDLL, POINTER, Structure, byref, c_char_p, c_int32, c_long, c_uint32, c_void_p


security = CDLL("/System/Library/Frameworks/Security.framework/Security")
foundation = CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
ITEM_NOT_FOUND = -25300
UTF8 = 0x08000100


class KeychainAttribute(Structure):
    _fields_ = [("tag", c_uint32), ("length", c_uint32), ("data", c_char_p)]


class KeychainAttributeList(Structure):
    _fields_ = [("count", c_uint32), ("attributes", POINTER(KeychainAttribute))]


def bind(library, name, result, *arguments):
    function = getattr(library, name)
    function.argtypes = arguments
    function.restype = result
    return function


find_item = bind(
    security, "SecKeychainFindGenericPassword", c_int32, c_void_p, c_uint32, c_char_p,
    c_uint32, c_char_p, c_void_p, c_void_p, POINTER(c_void_p),
)
modify_item = bind(security, "SecKeychainItemModifyContent", c_int32, c_void_p, c_void_p, c_uint32, c_char_p)
create_item = bind(
    security, "SecKeychainItemCreateFromContent", c_int32, c_uint32, POINTER(KeychainAttributeList),
    c_uint32, c_char_p, c_void_p, c_void_p, POINTER(c_void_p),
)
create_trusted_app = bind(security, "SecTrustedApplicationCreateFromPath", c_int32, c_char_p, POINTER(c_void_p))
create_access = bind(security, "SecAccessCreate", c_int32, c_void_p, c_void_p, POINTER(c_void_p))
create_string = bind(foundation, "CFStringCreateWithCString", c_void_p, c_void_p, c_char_p, c_uint32)
create_array = bind(foundation, "CFArrayCreate", c_void_p, c_void_p, POINTER(c_void_p), c_long, c_void_p)
release = bind(foundation, "CFRelease", None, c_void_p)


def check(status):
    if status != 0:
        raise OSError(status, "Klíčenka macOS")


def add_item(keychain, service, account, token):
    attributes = (KeychainAttribute * 3)(
        KeychainAttribute(int.from_bytes(b"svce", "big"), len(service), service),
        KeychainAttribute(int.from_bytes(b"acct", "big"), len(account), account),
        KeychainAttribute(int.from_bytes(b"labl", "big"), len(service), service),
    )
    attribute_list = KeychainAttributeList(len(attributes), attributes)
    with ExitStack() as references:
        # Keep the existing security(1) reader trusted alongside this Python process.
        applications = (c_void_p * 2)()
        for index, path in enumerate((b"/usr/bin/security", None)):
            application = c_void_p()
            check(create_trusted_app(path, byref(application)))
            references.callback(release, application)
            applications[index] = application.value

        descriptor = create_string(None, service, UTF8)
        if not descriptor:
            raise OSError("Klíčenka nemohla vytvořit název položky.")
        references.callback(release, descriptor)
        trusted = create_array(None, applications, len(applications), None)
        if not trusted:
            raise OSError("Klíčenka nemohla vytvořit seznam důvěryhodných aplikací.")
        references.callback(release, trusted)

        access = c_void_p()
        check(create_access(descriptor, trusted, byref(access)))
        references.callback(release, access)
        check(create_item(int.from_bytes(b"genp", "big"), byref(attribute_list), len(token), token, keychain, access, None))


def store_token(service, account, token, *, keychain=None):
    service, account, token = (value.encode("ascii") for value in (service, account, token))
    item = c_void_p()
    status = find_item(keychain, len(service), service, len(account), account, None, None, byref(item))
    if status == ITEM_NOT_FOUND:
        add_item(keychain, service, account, token)
        return
    check(status)
    try:
        check(modify_item(item, None, len(token), token))
    finally:
        release(item)
