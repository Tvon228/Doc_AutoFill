import { For } from "solid-js"
import classes from "./DropdownMenu.module.sass"

type DropdownMenuProps = {
	items: string[]
	selected: string
	isOpen: boolean
	isAnimating: boolean
	onSelect: (item: string) => void
}

export const DropdownMenu = (props: DropdownMenuProps) => {
	return (
		<div
			classList={{
				[classes.dropdown]: true,
				[classes.dropdownOpen]: props.isOpen,
				[classes.dropdownClosing]: props.isAnimating,
			}}
		>
			<For each={props.items}>
				{(item) => (
					<div
						class={classes.dropdownItem}
						classList={{
							[classes.selected]: props.selected === item,
						}}
						onClick={() => props.onSelect(item)}
					>
						{item}
					</div>
				)}
			</For>
		</div>
	)
}
