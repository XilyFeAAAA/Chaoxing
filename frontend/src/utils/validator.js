function checkEmail(userEmail){
  if (userEmail == "" || userEmail == null) {
    return {data: false, msg: '请输入邮箱'};
  }
  var mailreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
  if (!mailreg.test(userEmail)) {
    return {data: false, msg: '电子邮件格式不正确'};
  }
  return {data: true, msg: ''};
}

export default {
  checkEmail
}