import AddButton from "../../../ui/buttons/WorkArea/Add/addButton"
import classes from "./Specialists.module.sass"

import { VsCalendar } from 'solid-icons/vs'

export default function SpecialistsBlock() {
	return (
		<div class={classes.content}>
			<div class={classes.header}>
				<div class={classes.text}>Специалисты:</div>
				<AddButton />
			</div>
			<ol class={classes.items}> 
				<li class={classes.marker}>
					<div class={classes.information}>
						<input type="text" placeholder="ФИО"/>
						<input type="text" placeholder="Количество отработанных часов"/>
						<input type="text" placeholder="Рейт специалиста в час"/>
					</div>
				</li>
			</ol>
            <div class={classes.sum}>
                <span class={classes.text}>Рассчетная сумма:</span>
                <span class={classes.price}>115 000₽</span>
            </div>
            <div class={classes.reportingPeriod}>
                <span class={classes.text}>Отчетный период</span>
                <button class={classes.period}>
                    Февраль 2025 - март 2025
					<VsCalendar size={24} class="calendarIcn"/>
                </button>
            </div>
		</div>
	)
}
