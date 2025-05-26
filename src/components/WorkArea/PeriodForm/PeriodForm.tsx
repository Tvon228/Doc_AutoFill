import { createSignal } from "solid-js";
import classes from "./PeriodForm.module.sass";
import { VsCalendar } from 'solid-icons/vs';

export default function PeriodForm() {
    const [reportPeriod, setReportPeriod] = createSignal("1 мар 2025 - 31 мар 2025");
    const [workPeriod, setWorkPeriod] = createSignal("1 мар 2025 - 31 мар 2025");

    return (
        <div class={classes.container}>
            <div class={classes.field}>
                <label class={classes.label}>Отчётный период</label>
                <div class={classes.dateInput}>
                    <input
                        type="text"
                        class={classes.input}
                        value={reportPeriod()}
                        onInput={(e) => setReportPeriod(e.target.value)}
                        placeholder="1 мар 2025 - 31 мар 2025"
                    />
                    <VsCalendar size={18} class={classes.calendarIcon} />
                </div>
            </div>
            <div class={classes.field}>
                <label class={classes.label}>Срок выполнения работ</label>
                <div class={classes.dateInput}>
                    <input
                        type="text"
                        class={classes.input}
                        value={workPeriod()}
                        onInput={(e) => setWorkPeriod(e.target.value)}
                        placeholder="1 мар 2025 - 31 мар 2025"
                    />
                    <VsCalendar size={18} class={classes.calendarIcon} />
                </div>
            </div>
            <div class={classes.summary}>
                <span class={classes.label}>Рассчетная сумма:</span>
                <span class={classes.amount}>115 000 ₽</span>
            </div>
            <div class={classes.period}>
                <span class={classes.label}>Отчетный период:</span>
                <button class={classes.periodButton}>
                    Февраль 2025 - март 2025
                    <VsCalendar size={18} class={classes.calendarIcon} />
                </button>
            </div>
        </div>
    );
}