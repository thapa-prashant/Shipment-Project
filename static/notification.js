window.addEventListener('load', function () {
    if (window.Notification && Notification.permission !== "granted") {
      Notification.requestPermission(function (status) {
        if (Notification.permission !== status) {
          Notification.permission = status;
        }
      });
    }
  
    var button = document.getElementsByTagName('button')[0];
  
    button.addEventListener('click', function () {
      if (window.Notification && Notification.permission === "granted") {
        var notify = new Notification('Hi there!', {
            body: 'How are you doing? https://sarobartech.com',
            icon: 'https://sarobartech.com/media/organizationdetails/sarobar_logo_0DyqH7y.png',
        });
      }
      else if (window.Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function (status) {
          if (status === "granted") {
            var n = new Notification("Granted Granted Granted")
          }
        });
      }
  
      // If the user refuses to get notified
      else {
        // We can fallback to a regular modal alert
      }
    });
  });