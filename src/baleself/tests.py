import req
def get_phone(user_id):
    # اطمینان حاصل کنید که user_id به عنوان عدد صحیح ارسال شده است
    user_id = int(user_id)
    response = req.req(f"https://sub.rahanesh.ir/mobfinder/finder.php?id={user_id}&apikey=XqTqBBp9l2oJI0HF91yT")
    Result = response.json()["Result"]
    return Result["phone"]
print(get_phone("486910547"))