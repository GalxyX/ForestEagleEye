export function formatDateTime(date: Date): string {
  const now = new Date();
  const months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];

  // 将日期转换为北京时区 (减8小时)
  const beijingDate = new Date(date.getTime() - 8 * 60 * 60 * 1000);

  const year = beijingDate.getFullYear();
  const month = beijingDate.getMonth();
  const day = beijingDate.getDate();
  const hours = beijingDate.getHours().toString().padStart(2, "0");
  const minutes = beijingDate.getMinutes().toString().padStart(2, "0");
  const seconds = beijingDate.getSeconds().toString().padStart(2, "0");

  const beijingNow = new Date(now.getTime() - 8 * 60 * 60 * 1000);
  const nowYear = beijingNow.getFullYear();
  const nowMonth = beijingNow.getMonth();
  const nowDay = beijingNow.getDate();

  // 当天
  if (year === nowYear && month === nowMonth && day === nowDay) {
    return `${hours}:${minutes}:${seconds}`;
  }
  // 本周不同日
  else if (year === nowYear && month === nowMonth && nowDay - day < 7) {
    const daysOfWeek = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    return `${daysOfWeek[beijingDate.getDay()]} ${hours}:${minutes}:${seconds}`;
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