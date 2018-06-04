from base58 import b58encode, b58decode, b58encode_check
import string
#n58 = b'\x58'
from hashlib import new as hnew
from hashlib import sha512, sha256

NUM_TO_OP_CODES = {
  0: 'OP_0',
  76: 'OP_PUSHDATA1',
  77: 'OP_PUSHDATA2',
  78: 'OP_PUSHDATA4',
  79: 'OP_1NEGATE',
  80: 'OP_RESERVED',
  81: 'OP_1',
  82: 'OP_2',
  83: 'OP_3',
  84: 'OP_4',
  85: 'OP_5',
  86: 'OP_6',
  87: 'OP_7',
  88: 'OP_8',
  89: 'OP_9',
  90: 'OP_10',
  91: 'OP_11',
  92: 'OP_12',
  93: 'OP_13',
  94: 'OP_14',
  95: 'OP_15',
  96: 'OP_16',
  97: 'OP_NOP',
  98: 'OP_VER',
  99: 'OP_IF',
  100: 'OP_NOTIF',
  101: 'OP_VERIF',
  102: 'OP_VERNOTIF',
  103: 'OP_ELSE',
  104: 'OP_ENDIF',
  105: 'OP_VERIFY',
  106: 'OP_RETURN',
  107: 'OP_TOALTSTACK',
  108: 'OP_FROMALTSTACK',
  109: 'OP_2DROP',
  110: 'OP_2DUP',
  111: 'OP_3DUP',
  112: 'OP_2OVER',
  113: 'OP_2ROT',
  114: 'OP_2SWAP',
  115: 'OP_IFDUP',
  116: 'OP_DEPTH',
  117: 'OP_DROP',
  118: 'OP_DUP',
  119: 'OP_NIP',
  120: 'OP_OVER',
  121: 'OP_PICK',
  122: 'OP_ROLL',
  123: 'OP_ROT',
  124: 'OP_SWAP',
  125: 'OP_TUCK',
  126: 'OP_CAT',
  127: 'OP_SUBSTR',
  128: 'OP_LEFT',
  129: 'OP_RIGHT',
  130: 'OP_SIZE',
  131: 'OP_INVERT',
  132: 'OP_AND',
  133: 'OP_OR',
  134: 'OP_XOR',
  135: 'OP_EQUAL',
  136: 'OP_EQUALVERIFY',
  137: 'OP_RESERVED1',
  138: 'OP_RESERVED2',
  139: 'OP_1ADD',
  140: 'OP_1SUB',
  141: 'OP_2MUL',
  142: 'OP_2DIV',
  143: 'OP_NEGATE',
  144: 'OP_ABS',
  145: 'OP_NOT',
  146: 'OP_0NOTEQUAL',
  147: 'OP_ADD',
  148: 'OP_SUB',
  149: 'OP_MUL',
  150: 'OP_DIV',
  151: 'OP_MOD',
  152: 'OP_LSHIFT',
  153: 'OP_RSHIFT',
  154: 'OP_BOOLAND',
  155: 'OP_BOOLOR',
  156: 'OP_NUMEQUAL',
  157: 'OP_NUMEQUALVERIFY',
  158: 'OP_NUMNOTEQUAL',
  159: 'OP_LESSTHAN',
  160: 'OP_GREATERTHAN',
  161: 'OP_LESSTHANOREQUAL',
  162: 'OP_GREATERTHANOREQUAL',
  163: 'OP_MIN',
  164: 'OP_MAX',
  165: 'OP_WITHIN',
  166: 'OP_RIPEMD160',
  167: 'OP_SHA1',
  168: 'OP_SHA256',
  169: 'OP_HASH160',
  170: 'OP_HASH256',
  171: 'OP_CODESEPARATOR',
  172: 'OP_CHECKSIG',
  173: 'OP_CHECKSIGVERIFY',
  174: 'OP_CHECKMULTISIG',
  175: 'OP_CHECKMULTISIGVERIFY',
  176: 'OP_NOP1',
  177: 'OP_NOP2',
  177: 'OP_CHECKLOCKTIMEVERIFY',
  178: 'OP_NOP3',
  178: 'OP_CHECKSEQUENCEVERIFY',
  179: 'OP_NOP4',
  180: 'OP_NOP5',
  181: 'OP_NOP6',
  182: 'OP_NOP7',
  183: 'OP_NOP8',
  184: 'OP_NOP9',
  185: 'OP_NOP10',
  252: 'OP_NULLDATA',
  253: 'OP_PUBKEYHASH',
  254: 'OP_PUBKEY',
  255: 'OP_INVALIDOPCODE',
}

OP_CODES_TO_NUM= {v:k for k,v in NUM_TO_OP_CODES.items()}

def h160(inp):
  h1 = sha256(inp).digest()
  return hnew('ripemd160', h1).digest()


def hexscript_to_scripthash(hex_script):
    # hex_script is hex int form
    to_be_hashed = hex_script.to_bytes((hex_script.bit_length()+7)//8 ,'big')

    return h160(to_be_hashed)

scr = '1 042f90074d7a5bf30c72cf3a8dfd1381bdbd30407010e878f3a11269d5f74a58788505cdca22ea6eab7cfb40dc0e07aba200424ab0d79122a653ad0c7ec9896bdf 1 OP_CHECKMULTISIG'

# scr = '2 04C16B8698A9ABF84250A7C3EA7EEDEF9897D1C8C6ADF47F06CF73370D74DCCA01CDCA79DCC5C395' \
#       'D7EEC6984D83F1F50C900A24DD47F569FD4193AF5DE762C587 04A2192968D8655D6A935BEAF2CA23' \
#       'E3FB87A3495E7AF308EDF08DAC3C1FCBFC2C75B4B0F4D0B1B70CD2423657738C0C2B1D5CE65C97D7' \
#       '8D0E34224858008E8B49 047E63248B75DB7379BE9CDA8CE5751D16485F431E46117B9D0C1837C9D5' \
#     '737812F393DA7D4420D7E1A9162F0279CFC10F1E8E8F3020DECDBC3C0DD389D99779650421D65CBD' \
#     '7149B255382ED7F78E946580657EE6FDA162A187543A9D85BAAA93A4AB3A8F 044DADA618D0872274' \
#     '40645ABE8A35DA8C5B73997AD343BE5C2AFD94A5043752580AFA1ECED3C68D446BCAB69AC0BA7DF5' \
#     '0D56231BE0AABF1FDEEC78A6A45E394BA29A1EDF518C022DD618DA774D207D137AAB59E0B000EB7E' \
#     'D238F4D800 5 OP_CHECKMULTISIG'
#parse the script

def parse_script(script):
  split_script = script.split()
  hex_split = sum_bytes_literal([single_op_to_hex(t) for t in split_script]);
  return hex_split

#print(split_s)
def single_op_to_hex(w):
  if w in OP_CODES_TO_NUM:
    return OP_CODES_TO_NUM[w].to_bytes(1,'big')
  elif w.isdigit() and int(w)<=16:
    return (80+int(w)).to_bytes(1,'big')
  else:
    byte_length = (len(w)+1)//2;
    # print('****************')
    # print(len(w))
    # print(byte_length)
    # print('****************')
    # modificare se solo 1 byte basta o di più per il prefix
    return byte_length.to_bytes(1,'big') + int(w,16).to_bytes(byte_length,'big')

def sum_bytes_literal(ls):
    res = ls[0]
    for x in ls[1:]:
        res = res + x;
    return res


#
# print('OP_1 --->')
# print(hex(int.from_bytes(single_op_to_hex('OP_1'),byteorder='big')))
#
# print('3')
# print(hex(int.from_bytes(single_op_to_hex('3'),byteorder='big')))
#
# print('042f90074d7a5b')
# print(hex(int.from_bytes(single_op_to_hex('042f90074d7a5b'),byteorder='big')))
# print(single_op_to_hex('042f90074d7a5b'))

print(hex(int.from_bytes(single_op_to_hex('042f90074d7a5b'),byteorder='big')))

print(hex(int.from_bytes(parse_script(scr),byteorder='big')))



s_hex = 0x5141042f90074d7a5bf30c72cf3a8dfd1381bdbd30407010e878f3a11269d5f74a58788505cdca22ea6eab7cfb40dc0e07aba200424ab0d79122a653ad0c7ec9896bdf51ae

res = hex(int.from_bytes(hexscript_to_scripthash(s_hex),byteorder='big'))
print(res)
print(b58encode_check(b'\x05'+ hexscript_to_scripthash(s_hex)))

print(b58encode_check(b'\x6f'+h160( 0x0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6.to_bytes(65,'big'))))
print(hex(int.from_bytes(h160(     0x0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6.to_bytes(65,'big')),byteorder='big')))

