import classes from "./Header.module.sass"

import { BsQuestionCircleFill } from "solid-icons/bs"
import { FiSearch } from "solid-icons/fi"

function Header() {
	return (
		<div class={classes.container}>
			<div class={classes.content}>
				<div class={classes.documentControls}>
					<div class={classes.nameProject}>
						<h1>
							<span class={classes.documentAuto}>
								Document Auto
							</span>
							<span class={classes.fill}>Fill</span>
						</h1>
					</div>
					<div class={classes.search}>
						<input
							class={classes.searchInput}
							placeholder="Поиск шаблонов"
						/>
						<FiSearch size={20} color="#3B3B3B" class={classes.searchIcon}/>
					</div>
				</div>
				<div class={classes.questionMark}>
					<BsQuestionCircleFill size={27} color="#2C60F0" />
				</div>
			</div>
		</div>
	)
}

export default Header
