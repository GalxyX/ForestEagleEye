export function formatDateTime(date: Date): string {
  const now = new Date();
  const months = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];

  const year = date.getFullYear();
  const month = date.getMonth();
  const day = date.getDate();
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");

  const nowYear = now.getFullYear();
  const nowMonth = now.getMonth();
  const nowDay = now.getDate();

  // 当天
  if (year === nowYear && month === nowMonth && day === nowDay) {
    return `${hours}:${minutes}:${seconds}`;
  }
  // 本周不同日
  else if (year === nowYear && month === nowMonth && nowDay - day < 7) {
    const daysOfWeek = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    return `${daysOfWeek[date.getDay()]} ${hours}:${minutes}:${seconds}`;
  }
  // 本月不同日
  else if (year === nowYear && month === nowMonth) {
    // return `${day.toString().padStart(2, "0")} ${hours}:${minutes}:${seconds}`;
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