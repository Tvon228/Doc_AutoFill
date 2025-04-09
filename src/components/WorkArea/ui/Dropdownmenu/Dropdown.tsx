import { createSignal, onCleanup, createEffect } from "solid-js"
import { RiArrowsExpandUpDownLine } from "solid-icons/ri"
import classes from "./Dropdown.module.sass"

export default function Dropdown() {
	const [isOpen, setIsOpen] = createSignal(false)
	const [selected, setSelected] = createSignal("Выберите шаблон")

	const handleClickOutside = (event: MouseEvent) => {
		const dropdown = document.querySelector(`.${classes.dropdown}`)
		if (dropdown && !dropdown.contains(event.target as Node)) {
			setIsOpen(false)
		}
	}

	createEffect(() => {
		if (isOpen()) {
			document.addEventListener("click", handleClickOutside)
		} else {
			document.removeEventListener("click", handleClickOutside)
		}
	})

	onCleanup(() => {
		document.removeEventListener("click", handleClickOutside)
	})

	return (
		<div class={classes.dropdown}>
			<div class={classes.text}>Шаблон документа:</div>
			<button
				class={classes.dropdownButton}
				onClick={() => setIsOpen(!isOpen())}
				classList={{
					[classes.selected]: selected() !== "Выберите шаблон",
				}}
			>
				{selected()}
				<RiArrowsExpandUpDownLine
					size={16}
					classList={{
						[classes.icon]: true,
						[classes.iconOpen]: isOpen(),
					}}
				/>
			</button>
			<div
				classList={{
					[classes.dropdownContent]: true,
					[classes.show]: isOpen(),
				}}
			>
				<a
					onClick={() => setSelected("Акт")}
					classList={{
						[classes.active]: selected() === "Акт",
					}}
				>
					Акт
				</a>
				<a
					onClick={() => setSelected("Заказ")}
					classList={{ [classes.active]: selected() === "Заказ" }}
				>
					Заказ
				</a>
			</div>
		</div>
	)
}
