window.addEventListener('load',()=>{

    //Function to create a post
    async function create_post(data) {
        let options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "omit",
            body: JSON.stringify(data)
        }

        let res  = {
            "status":"",
            "body": ""
        }
        const response = await fetch(API_CREATE_POST, options)
        let info = await response.json()
        if (response.status == 200){
            res = {
                "status": response.status,
                "body":info
            }
                return res
        }else{
            return info.message
        }
    }

    const API_CREATE_POST = "http://127.0.0.1:5001/api/foro/post/crear"
    let create_new_form = document.getElementById('create_new')
    let title_new = document.getElementById('title_new')
    let description_new = document.getElementById('description')
    let charge_image = document.getElementById('charge_image')
    create_new_form.addEventListener('submit',async(e)=>{
        e.preventDefault()
        let title = title_new.value
        let description = description_new.value
        let response = await create_post({"title":title,"description":description,
                                        "token":localStorage.getItem('token')})
        window.location.href = '/foro/post/'+response.body.response.newPost.id
        
    })
})