from flask import make_response, jsonify
def unauthorized():
    result={"error":
              {"msg": "401 error: Kullanıcı adı veya şifreniz yanlış."}
              }
    response=jsonify({'result': result})
    return make_response(response,401)