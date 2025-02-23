import { createSignal, Show, For } from "solid-js"
import classes from "./MyDoc.module.sass"
import { FiUsers, FiClock } from "solid-icons/fi"
import { AiOutlineFile } from "solid-icons/ai"
import { RiArrowsArrowRightSLine, RiArrowsArrowDownSLine } from "solid-icons/ri"
import MyDocsButton from "../../ui/buttons/MyDocButton"

function MyDocs() {
	const [isJuridicalOpen, setJuridicalOpen] = createSignal(false)
	const [isAnimating, setIsAnimating] = createSignal(false)
	const [selectedEntity, setSelectedEntity] = createSignal("")

	const juridicalList = ["Аниме", "Байт", "Жираф", "Мега"]

	const handleJuridicalClick = () => {
		if (isAnimating()) return
		setIsAnimating(true)
		setJuridicalOpen(!isJuridicalOpen())

		// Сброс флага анимации после завершения
		setTimeout(() => setIsAnimating(false), 300)
	}

	const startClosingAnimation = () => {
		if (isAnimating()) return
		setIsAnimating(true)
		setJuridicalOpen(false)
		setTimeout(() => setIsAnimating(false), 300)
	}

	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.header}>
					<h2 class={classes.title}>Мои документы</h2>
				</div>

				<div class={classes.navSection}>
					{/* Блок Юр.лица */}
					<div class={classes.navItemWrapper}>
						<div
							class={classes.navItem}
							onClick={handleJuridicalClick}
							role="button"
							aria-expanded={isJuridicalOpen()}
						>
							<div class={classes.itemContent}>
								<FiUsers class={classes.icon} size={24} />

								<span class={classes.itemText}>Юр.лица</span>
							</div>
							<div class={classes.arrow}>
								{isJuridicalOpen() ? (
									<RiArrowsArrowDownSLine size={20} />
								) : (
									<RiArrowsArrowRightSLine size={20} />
								)}
							</div>
						</div>

						<div
							classList={{
								[classes.dropdown]: true,
								[classes.dropdownOpen]: isJuridicalOpen(),
								[classes.dropdownClosing]:
									!isJuridicalOpen() && isAnimating(),
							}}
						>
							<For each={juridicalList}>
								{(entity) => (
									<div
										class={classes.dropdownItem}
										classList={{
											[classes.selected]:
												selectedEntity() === entity,
										}}
										onClick={() =>
											setSelectedEntity(entity)
										}
									>
										{entity}
									</div>
								)}
							</For>
						</div>
					</div>

					{/* Остальные пункты */}
					<div class={classes.navItem}>
						<div class={classes.itemContent}>
							<FiClock class={classes.icon} size={24} />
							<span class={classes.itemText}>Недавние</span>
						</div>
						<RiArrowsArrowRightSLine
							class={classes.arrow}
							size={20}
						/>
					</div>

					<div class={classes.navItem}>
						<div class={classes.itemContent}>
							<AiOutlineFile class={classes.icon} size={24} />
							<span class={classes.itemText}>Архив</span>
						</div>
						<RiArrowsArrowRightSLine
							class={classes.arrow}
							size={20}
						/>
					</div>
				</div>

				<div class={classes.footer}>
					<MyDocsButton onClick={startClosingAnimation} />
				</div>
			</div>
		</div>
	)
}

export default MyDocs
