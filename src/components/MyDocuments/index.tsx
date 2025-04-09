import classes from "./MyDoc.module.sass"

import { createSignal } from "solid-js"

import { FiUsers, FiClock } from "solid-icons/fi"
import { AiOutlineFile } from "solid-icons/ai"
import { RiArrowsArrowRightSLine } from "solid-icons/ri"

import { NavItem } from "./ui/NavItem"
import { DropdownMenu } from "./ui/DropdownMenu"
import { useDropdownAnimation } from "./ui/hooks/useDropdownAnimation"

import MyDocsButton from "../ui/buttons/MyDocButton"

const MyDocuments = () => {
	const [isJuridicalOpen, setJuridicalOpen] = createSignal(false)
	const [selectedEntity, setSelectedEntity] = createSignal("")
	const { isAnimating, startAnimation } = useDropdownAnimation()
	const juridicalList = ["Аниме", "Байт", "Жираф", "Мега"]

	const handleJuridicalClick = () => {
		startAnimation(() => setJuridicalOpen(!isJuridicalOpen()))
	}

	const startClosingAnimation = () => {
		startAnimation(() => setJuridicalOpen(false))
	}

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.header}>
					<h2 class={classes.title}>Мои документы</h2>
				</div>

				<div class={classes.navSection}>
					<div class={classes.navItemWrapper}>
						<NavItem
							icon={FiUsers}
							text="Юр.лица"
							arrowRightIcon={RiArrowsArrowRightSLine}
							isDropdown
							isOpen={isJuridicalOpen()}
							onClick={handleJuridicalClick}
						/>

						<DropdownMenu
							items={juridicalList}
							selected={selectedEntity()}
							isOpen={isJuridicalOpen()}
							isAnimating={isAnimating()}
							onSelect={setSelectedEntity}
						/>
					</div>
					<NavItem
						icon={FiClock}
						text="Недавние"
						arrowRightIcon={RiArrowsArrowRightSLine}
						isDropdown={true}
					/>
					<NavItem
						icon={AiOutlineFile}
						text="Архив"
						arrowRightIcon={RiArrowsArrowRightSLine}
						isDropdown={true}
					/>
				</div>

				<div class={classes.footer}>
					<MyDocsButton onClick={startClosingAnimation} />
				</div>
			</div>
		</div>
	)
}

export default MyDocuments
