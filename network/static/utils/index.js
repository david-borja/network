export const $ = (selector) => document.querySelector(selector)

export const $$ = (selector) => document.querySelectorAll(selector)

export const mimicDjangoDateString = (isoString) => {
  const utcNow = new Date(isoString)
  utcNow.setMinutes(utcNow.getMinutes() + utcNow.getTimezoneOffset())
  const date = new Date(utcNow)

  const options = {
    month: 'short', // "Nov" for November
    day: 'numeric', // Day of the month without leading zero
    year: 'numeric', // Full year
    hour: 'numeric', // Hour (12-hour format)
    minute: '2-digit', // Minute with leading zero
    hour12: true, // 12-hour format with a.m./p.m.
  }

  const formattedDate = new Intl.DateTimeFormat('en-US', options).format(date)
  const dividedString = formattedDate.split(' ')
  const monthIndex = 0
  const hour12FormatIndex = dividedString.length - 1
  const { [monthIndex]: month, [hour12FormatIndex]: hour12Format } = dividedString
  const formattedMonth = month.concat('.')
  const formattedHour12Format = hour12Format
    .toLowerCase()
    .split('')
    .join('.')
    .concat('.')
  const dividedStringWithoutEdgeIndexes = dividedString.slice(
    1,
    dividedString.length - 1
  )
  const result = [
    formattedMonth,
    ...dividedStringWithoutEdgeIndexes,
    formattedHour12Format,
  ].join(' ')
  return result
}
