import { splitProps } from "solid-js"
import classes from "./NavItem.module.sass"

type NavItemProps = {
	icon: any
	text: string
	arrowRightIcon?: any
	isDropdown?: boolean
	isOpen?: boolean
	onClick?: () => void
}

export const NavItem = (props: NavItemProps) => {
	const [local] = splitProps(props, [
		"icon",
		"text",
		"arrowRightIcon",
		"isDropdown",
		"isOpen",
		"onClick",
	])

	return (
		<div
			class={classes.navItem}
			onClick={local.onClick}
			role={local.onClick ? "button" : undefined}
			aria-expanded={local.isOpen}
		>
			<div class={classes.itemContent}>
				<local.icon class={classes.icon} size={24} />
				<span class={classes.itemText}>{local.text}</span>
			</div>
			{local.isDropdown && (
				<div class={classes.arrow}>
					{local.isOpen ? (
						<local.arrowRightIcon size={20} />
					) : (
						<local.arrowRightIcon size={20} />
					)}
				</div>
			)}
		</div>
	)
}
