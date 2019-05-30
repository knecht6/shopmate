const renuew=()=>{
    console.log("Renewing Token")
    fetch('http://40.113.199.165:3000/api/token/refresh/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "refresh": localStorage.getItem('refresh')
        })
      }).then(resolve => {
        console.log(resolve.status);
          return resolve.json();
          
      }).then(data=>{
          console.log(data.access);
          localStorage.setItem('access', data.access);
          console.log(localStorage.getItem('access'));
          window.location.reload()
          console.log(data.status);
      });
}

export default renuew;