#  ___________________________________________________________________
# |=-=-=-=-=-=-=-=-=-=-=-=-=-| ERRORS LIST |-=-=-=-=-=-=-=-=-=-=-=-=-=|
# | This File is for storing my Error codes to do with the application|
# | being stored seperately as of "separations of concerns" designing |
#  \_________________________________________________________________/

ERRORS = {
    "UNSUPPORTED_FILE_TYPE": "APP ERROR! - Error 01: File type not supported by the application.",
    "INSUFFICIENT_CONTENTS": "APP ERROR! - Error 02: File contains less than 50 words. Fallback To Use Metadata",
    "FILE_NOT_FOUND": "APP ERROR! - Error 03: File couldn't be located at given path.",
    "METADATA_NOT_FOUND": "APP ERROR! - Error 04: Metadata couldn't be found or accessed by application",
    "PARSE_FAILED": "APP ERROR! - Error 05: Mistral7bs Response Failed To Be Parsed.",
    "UNSUPPORTED_IMAGEorSCANNED_PDF": "APP ERROR! - Error 06: PDF is Likely Scanned or Image Based, which is Currently Unsupported."
}
