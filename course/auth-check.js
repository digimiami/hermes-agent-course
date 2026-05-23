// Course Auth Check — include on every course page
(function() {
  var password = "HERMES-XK7M-PQ92";
  var authed = localStorage.getItem("hermes_course_auth");
  
  if (authed !== password) {
    // Not authenticated — redirect to login
    var loginUrl = "login.html";
    // Preserve where they were going
    var dest = window.location.pathname.replace("/course/", "") || "index.html";
    window.location.href = loginUrl + "?redirect=" + encodeURIComponent(dest);
  }
})();
