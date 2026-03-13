import requests
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3

# SSL Warning বন্ধ করার জন্য
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =====================================================================
# ⚙️ সেন্ট্রাল গেম কনফিগারেশন (যেকোনো আপডেটে শুধুমাত্র এই অংশটি পরিবর্তন করবেন)
# =====================================================================
class GameConfig:
    # গেম ভার্সন এবং এপিআই ডিটেইলস
    RELEASE_VERSION = "OB52"
    UNITY_VERSION = "2018.4.11f1"
    USER_AGENT = "Dalvik/2.1.0 (Linux; U; Android 10; ASUS_Z01QD Build/QP1A.190711.020)"
    
    # এনক্রিপশন কি (Keys & IVs)
    GAME_KEY = b'Yg&tc%DEuh6%Zc^8'
    GAME_IV = b'6oyZDr22E3ychjM%'
    
    # এপিআই ইউআরএল
    HOST_URL = "clientbp.ggblueshark.com"
    BASE_URL = f"https://{HOST_URL}"

    @classmethod
    def get_headers(cls, token=None):
        """ডাইনামিক হেডার জেনারেট করার ফাংশন"""
        headers = {
            "User-Agent": cls.USER_AGENT,
            "X-Unity-Version": cls.UNITY_VERSION,
            "ReleaseVersion": cls.RELEASE_VERSION,
            "X-GA": "v1 1",
            "Connection": "keep-alive",
            "Host": cls.HOST_URL
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers


# =====================================================================
# 🛠️ এনক্রিপশন এবং কোর ইউটিলিটি ফাংশন
# =====================================================================
class SecurityUtils:
    @staticmethod
    def encrypt_aes_game(plain_text_hex):
        """গেম ডেটা AES দিয়ে এনক্রিপ্ট করার ফাংশন"""
        try:
            plain_text = bytes.fromhex(plain_text_hex)
            cipher = AES.new(GameConfig.GAME_KEY, AES.MODE_CBC, GameConfig.GAME_IV)
            cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
            return cipher_text.hex()
        except Exception as e:
            return None

    @staticmethod
    def encode_varint(value):
        """ইন্টিজার ভ্যালুকে Varint হেক্স ফরম্যাটে রূপান্তর করার ফাংশন"""
        try:
            value = int(value)
            out = []
            while (value & 0xffffffffffffff80) != 0:
                out.append((value & 0x7f) | 0x80)
                value >>= 7
            out.append(value & 0x7f)
            return bytes(out).hex()
        except Exception:
            return ""

    @staticmethod
    def encrypt_target_id(x):
        """ফ্রেন্ড রিকোয়েস্টের জন্য টার্গেট ইউআইডি এনক্রিপ্ট করার স্পেশাল ফাংশন"""
        try:
            x = int(x)
            dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
            xxx = ['1', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
            
            x = x / 128
            if x > 128:
                x = x / 128
                if x > 128:
                    x = x / 128
                    if x > 128:
                        x = x / 128
                        strx = int(x)
                        y = (x - int(strx)) * 128
                        z = (y - int(str(int(y)))) * 128
                        n = (z - int(str(int(z)))) * 128
                        m = (n - int(str(int(n)))) * 128
                        return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
                    else:
                        strx = int(x)
                        y = (x - int(strx)) * 128
                        z = (y - int(str(int(y)))) * 128
                        n = (z - int(str(int(z)))) * 128
                        return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            return ""
        except Exception:
            return ""


# =====================================================================
# 🚀 মেইন এপিআই অ্যাকশন ফাংশন (Add & Remove)
# =====================================================================
class FriendManager:
    @staticmethod
    def action_add_friend(token, target_uid):
        """ফ্রেন্ড রিকোয়েস্ট পাঠানোর প্রোডাকশন-রেডি ফাংশন"""
        if not token or not target_uid:
            return False, "Invalid Token or Target UID"

        try:
            url = f"{GameConfig.BASE_URL}/RequestAddingFriend"
            headers = GameConfig.get_headers(token)
            
            enc_id = SecurityUtils.encrypt_target_id(target_uid)
            if not enc_id:
                return False, "Target ID Encryption Failed"
                
            plain_payload = "08c8b5cfea1810" + enc_id + "18012008"
            encrypted_body = SecurityUtils.encrypt_aes_game(plain_payload)
            
            if not encrypted_body:
                return False, "Payload Encryption Failed"

            resp = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_body), verify=False, timeout=15)
            
            if resp.status_code == 200:
                return True, f"Request successfully sent to {target_uid}"
            else:
                return False, f"Server Error: {resp.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network Connection Error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected Error: {str(e)}"

    @staticmethod
    def action_remove_friend(token, my_uid, target_uid):
        """ফ্রেন্ডলিস্ট থেকে ডিলিট করার প্রোডাকশন-রেডি ফাংশন"""
        if not token or not my_uid or not target_uid:
            return False, "Missing required credentials or IDs"

        try:
            url = f"{GameConfig.BASE_URL}/RemoveFriend"
            headers = GameConfig.get_headers(token)
            
            my_uid_enc = SecurityUtils.encode_varint(my_uid)
            target_uid_enc = SecurityUtils.encode_varint(target_uid)
            
            plain_payload = "08" + my_uid_enc + "10" + target_uid_enc
            encrypted_body = SecurityUtils.encrypt_aes_game(plain_payload)
            
            if not encrypted_body:
                return False, "Payload Encryption Failed"

            resp = requests.post(url, headers=headers, data=bytes.fromhex(encrypted_body), verify=False, timeout=15)
            
            if resp.status_code == 200:
                return True, f"Successfully removed {target_uid} from friend list"
            elif resp.status_code == 400:
                return False, f"UID {target_uid} is not in your friend list"
            else:
                return False, f"Server Error: {resp.status_code}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network Connection Error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected Error: {str(e)}"
