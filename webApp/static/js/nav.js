window.addEventListener('load', async()=>{
    async function get_user(token){
        const response = await fetch(API_REST,{method:'GET',
        headers: {'Authorization': 'Bearer '+token}})
        return response.json()
    }

    async function close_session(token){
        let options = {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(token)
        }
        const response = await fetch(LOG_OUT_API, options)
        return response.status
    }
    

    const API_NEWS = "http://127.0.0.1:5001/api/noticias"
    let navBar = document.getElementById('navBar')
    
    const LOG_OUT_API = "http://127.0.0.1:5001/api/usuario/cerrar_sesion"
    const API_REST = "http://127.0.0.1:5001/api/verify/token"
    if (localStorage.getItem('token')){
            let user_name = await get_user(localStorage.getItem('token'))
            navBar.innerHTML = `
            <div id="menu">
            <a href="/home"><img src="/static/img/definitivo.svg" alt="planeta con naturaleza"></a>
            <ul id="main_menu">
                <li><a href="/home">Sobre nosotros</a></li>
                <li><a href="/noticias">Noticias</a></li>
                <li><a href="/foro">Foro</a></li>

                <li>
                    <span id="user_menu">${user_name.user_name}<i class="fas fa-sort-down"></i></span>
                    </i>
                    <ul id="sub_menu">
                        <li id="m1"><a href="/usuario/perfil/${user_name.user_name}">Perfil</a></li>
                        <li id="m2"><a href="#">Cerrar sesion</a></li>
                    </ul>
                </li>
            </ul>
        </div>
        <div id="bars"><i class="fas fa-bars"></i></div>
        `

        let menu = document.getElementById('user_menu')
        let main_menu = document.getElementById('main_menu')
        let sub_menu = document.getElementById('sub_menu')
        let bars = document.getElementById('bars')
        let profile = document.getElementById('m1');
        let log_out = document.getElementById('m2');

        log_out.addEventListener('click', async()=>{
            let status = await close_session({'token':localStorage.getItem('token')})
            if (status == 200){
                localStorage.removeItem('token');
                window.location.href = '/home'
            }
        })

        user_menu.addEventListener('click',()=>{
            sub_menu.classList.toggle('sub_menu')
        })

        bars.addEventListener('click',()=>{
            main_menu.classList.toggle('main_menu')
        })

    }else{
        bars.addEventListener('click',()=>{
            main_menu.classList.toggle('main_menu')
        })
    }

})