import classes from "./DocView.module.sass"

import Doc from "../../assets/user.webp"

export default function DocView(){
    return(
        <div class={classes.container}>
            <div class={classes.content}>
                <div class={classes.header}>
                    <span class={classes.title}>Предпросмотр</span>
                </div>
                <div class={classes.docImg}>
                    <img src={Doc} alt="Документ" class={classes.img}/>
                </div>
            </div>
        </div>
    )
}