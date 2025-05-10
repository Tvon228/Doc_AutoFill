import { auth } from "../../../stores/authStore"
import classes from "./EditProfileModal.module.sass"

import { AiOutlineUser } from "solid-icons/ai"
import { IoCloseOutline } from 'solid-icons/io'

interface FormData {
    phone: string
    email: string
}

interface EditProfileModalProps {
    isOpen: boolean
    onClose: () => void
    formData: FormData
    setFormData: (data: FormData) => void
    onSubmit: (e: Event) => void
}

export default function EditProfileModal(props: EditProfileModalProps) {
    return (
        <>
            {props.isOpen && (
                <div classList={{
                    [classes.modalOverlay]: true,
                    [classes.open]: props.isOpen
                }}
                    style={{ display: props.isOpen ? "block" : "none" }}
                >
                    <div classList={{
                        [classes.modal]: true,
                        [classes.open]: props.isOpen
                    }}>
                        <div class={classes.modalHeader}>
                            <AiOutlineUser size={27} class={classes.imageUser} />
                            <div class={classes.infoPerson}>
                                <span class={classes.nameUser}>{auth.user?.name}</span>
                                <span>{auth.user?.position}</span>
                            </div>
                            <div class={classes.closeModal} onClick={props.onClose}>
                                <IoCloseOutline size={27} color=" #FF2400" />
                            </div>
                        </div>
                        <form class={classes.modalForm} onSubmit={props.onSubmit}>
                            <label>
                                Изменить телефон:
                                <input
                                    type="tel"
                                    value={props.formData.phone}
                                    onInput={(e) =>
                                        props.setFormData({
                                            ...props.formData,
                                            phone: e.currentTarget.value,
                                        })
                                    }
                                />
                            </label>
                            <label>
                                Изменить email:
                                <input
                                    type="email"
                                    value={props.formData.email}
                                    onInput={(e) =>
                                        props.setFormData({
                                            ...props.formData,
                                            email: e.currentTarget.value,
                                        })
                                    }
                                />
                            </label>
                            <div class={classes.footer}>
                                <button class={classes.modalButtons} type="submit">
                                    Подтвердить профиль
                                </button>
                            </div>
                        </form>
                    </div>
                </div >
            )
            }
        </>
    )
}