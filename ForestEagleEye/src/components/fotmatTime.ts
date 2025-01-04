export function formatDateTime(date: Date, isGMT: boolean = true): string {
  const now = new Date();
  const months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
  
  // 条件转换为北京时区
  const targetDate = isGMT ? new Date(date.getTime() - 8 * 60 * 60 * 1000) : date;

  const year = targetDate.getFullYear();
  const month = targetDate.getMonth();
  const day = targetDate.getDate();
  const hours = targetDate.getHours().toString().padStart(2, "0");
  const minutes = targetDate.getMinutes().toString().padStart(2, "0");
  const seconds = targetDate.getSeconds().toString().padStart(2, "0");

  const targetNow = isGMT ? new Date(now.getTime()) : now;
  const nowYear = targetNow.getFullYear();
  const nowMonth = targetNow.getMonth();
  const nowDay = targetNow.getDate();

  console.log(targetDate, targetNow);
  console.log(nowDay, day, nowDay - day);
  // 当天
  if (year === nowYear && month === nowMonth && day === nowDay) {
    return `${hours}:${minutes}:${seconds}`;
  }
  // 本周不同日
  else if (year === nowYear && month === nowMonth && nowDay - day < 7) {
    const daysOfWeek = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    return `${daysOfWeek[targetDate.getDay()]} ${hours}:${minutes}:${seconds}`;
  }
  // 本月不同日
  else if (year === nowYear && month === nowMonth) {
    return `${months[month]} ${day.toString().padStart(2, "0")} ${hours}:${minutes}:${seconds}`;
  }
  // 本年不同月
  else if (year === nowYear) {
    return `${months[month]}.${day.toString().padStart(2, "0")} ${hours}:${minutes}:${seconds}`;
  }
  // 非本年
  else {
    return `${year}.${months[month]}.${day.toString().padStart(2, "0")} ${hours}:${minutes}:${seconds}`;
  }
}