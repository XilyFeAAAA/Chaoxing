export function calculateDaysFromTimestamp(timestamp) {
    var now = Date.now() // 获取当前时间戳
    var difference = now - timestamp // 计算时间差（单位：毫秒）
    var millisecondsPerDay = 24 * 60 * 60 * 1000 // 一天的毫秒数
    var days = Math.floor(difference / millisecondsPerDay) // 计算天数差并取整
    return days
}

export function formatTimestamp(timestamp) {
    var date = new Date(timestamp)
    var year = date.getFullYear()
    var month = ('0' + (date.getMonth() + 1)).slice(-2)
    var day = ('0' + date.getDate()).slice(-2)
    var hours = ('0' + date.getHours()).slice(-2)
    var minutes = ('0' + date.getMinutes()).slice(-2)

    var formattedDate = year + '-' + month + '-' + day
    var formattedTime = hours + ':' + minutes

    return formattedDate + ' ' + formattedTime
}


export function getTimeAgo(timestamp) {
  var currentTime = Date.now(); // 当前时间戳，单位：秒
  var timeDifference = currentTime - timestamp; // 时间差，单位：秒

  if (timeDifference < 60) {
    return timeDifference + "秒之前";
  } else if (timeDifference < 3600) {
    var minutes = Math.floor(timeDifference / 60);
    return minutes + "分钟之前";
  } else {
    return "很久之前";
  }
}