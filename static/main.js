// Scripts for slide out menu

var sideNav = document.getElementById('side-nav');
var dateChooser = document.getElementById('date-chooser');

function openMenu() {
  sideNav.style.width = '320px';
  dateChooser.style.marginLeft = '25%';
}

function closeMenu() {
  sideNav.style.width = '0';
  dateChooser.style.marginLeft = '15%';
}

window.addEventListener('click', outsideClick);

// Scripts for modal iframe windows
var modalWindow = document.getElementById('modal-window');
var modaliFrame = document.getElementById('modal-iframe');
var closeButton = document.getElementById('btn-close');

closeButton.addEventListener('click', closeDate);

window.addEventListener('click', outsideClick);

function openDate(year, month, day) {
  // set blank modal display; set src of iframe so that it loads...
  modaliFrame.src = '/' + year + '-' + month + '-' + day;
  modalWindow.style.display = 'block';
}

function closeDate() {
  parent.location.reload();
}

function outsideClick (e) {
  if (e.target == modalWindow) {
    modalWindow.style.display = 'none';
  }
}
