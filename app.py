from flask import Flask, request, jsonify, render_template
from ff_api_manager import FriendManager

app = Flask(__name__)

# 🌐 হোমপেজ রুট
@app.route('/')
def home():
    return render_template('index.html')

# 🚀 সমস্ত অ্যাকশন হ্যান্ডেল করার জন্য একটি সাধারণ এন্ডপয়েন্ট
@app.route('/api/handle_action', methods=['POST'])
def api_handle_action():
    data = request.json
    
    # ইনপুট ডেটা
    action_type = data.get('action_type') # 'add' or 'remove'
    login_method = data.get('login_method') # 'token' or 'uid_pass'
    token = data.get('token')
    my_uid = data.get('my_uid')
    target_uid = data.get('target_uid')
    
    # এই সংস্করণে ইউআইডি/পাসওয়ার্ড দিয়ে লগইন করার ফাংশনটি নেই, তাই
    # শুধু টোকেন পদ্ধতিটিই কার্যকরী থাকবে।
    
    if login_method == 'token':
        if not token or not target_uid:
            return jsonify({"success": False, "message": "টোকেন এবং টার্গেট ইউআইডি প্রয়োজন।"})
            
        if action_type == 'add':
            # সেন্ট্রালাইজড ফাংশন কল
            success, message = FriendManager.action_add_friend(token, target_uid)
            return jsonify({"success": success, "message": message})
            
        elif action_type == 'remove':
            if not my_uid:
                return jsonify({"success": False, "message": "আপনার নিজের ইউআইডি প্রয়োজন।"})
            # সেন্ট্রালাইজড ফাংশন কল
            success, message = FriendManager.action_remove_friend(token, my_uid, target_uid)
            return jsonify({"success": success, "message": message})
            
        else:
            return jsonify({"success": False, "message": "অজানা অ্যাকশন।"})
            
    elif login_method == 'uid_pass':
        # ইউআইডি/পাসওয়ার্ড দিয়ে লগইন করার ফাংশনটি এই সংস্করণে তৈরি করা নেই।
        # এখানে আপনাকে আপনার লগইন করার লজিক লিখতে হবে যা একটি টোকেন তৈরি করবে।
        return jsonify({"success": False, "message": "'ইউআইডি + পাসওয়ার্ড' পদ্ধতিটি এখনও যুক্ত করা হয়নি। শুধুমাত্র 'টোকেন' পদ্ধতিটি ব্যবহার করুন।"})
    
    else:
        return jsonify({"success": False, "message": "অজানা লগইন পদ্ধতি।"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
