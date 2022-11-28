// DropDown
function DropDown() {
  let arrow = document.querySelectorAll(".arrow");
  for (var i = 0; i < arrow.length; i++) {
    arrow[i].addEventListener("click", (e) => {
      let arrowParent = e.target.parentElement.parentElement; //selecting main parent of arrow
      arrowParent.classList.toggle("showMenu");
    });
  }
  let sidebar = document.querySelector(".sidebar");
  let sidebarBtn = document.querySelector(".bx-menu");
  console.log(sidebarBtn);
  sidebarBtn.addEventListener("click", () => {
    sidebar.classList.toggle("close");
  });
}
//Clock count down
function Clock(secValue, minValue, hourValue, dayValue) {
  const seconds = document.querySelector(".seconds .number"),
    minutes = document.querySelector(".minutes .number"),
    hours = document.querySelector(".hours .number"),
    days = document.querySelector(".days .number");

  const timeFunction = setInterval(() => {
    secValue--;

    if (secValue === 0) {
      minValue--;
      secValue = 60;
    }
    if (minValue === 0) {
      hourValue--;
      minValue = 60;
    }
    if (hourValue === 0) {
      dayValue--;
      hourValue = 24;
    }

    if (dayValue === 0) {
      clearInterval(timeFunction);
    }
    seconds.textContent = secValue < 10 ? `0${secValue}` : secValue;
    minutes.textContent = minValue < 10 ? `0${minValue}` : minValue;
    hours.textContent = hourValue < 10 ? `0${hourValue}` : hourValue;
    days.textContent = dayValue < 10 ? `0${dayValue}` : dayValue;
  }, 1000); //1000ms = 1s
}

