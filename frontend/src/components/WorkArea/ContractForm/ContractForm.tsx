import { createSignal } from "solid-js";
import classes from "./ContractForm.module.sass";

import { VsCalendar } from 'solid-icons/vs'; // Предполагаю, что ты используешь эту библиотеку для иконок

export default function ContractForm() {
    const [contractName, setContractName] = createSignal("");
    const [contractDate, setContractDate] = createSignal("");
    const [orderNumber, setOrderNumber] = createSignal("");
    const [executor, setExecutor] = createSignal("");
    const [customer, setCustomer] = createSignal("");
    const [vat, setVat] = createSignal("");

    return (
        <div class={classes.container}>
            <div class={classes.field}>
                <label class={classes.label}>Номер договора</label>
                <input
                    type="text"
                    class={classes.input}
                    value={contractName()}
                    onInput={(e) => setContractName(e.target.value)}
                    placeholder="НФХХХ"
                />
            </div>
            <div class={classes.field}>
                <label class={classes.label}>Дата договора</label>
                <div class={classes.dateInput}>
                    <input
                        type="text"
                        class={classes.input}
                        value={contractDate()}
                        onInput={(e) => setContractDate(e.target.value)}
                        placeholder="9 сентября 2001"
                    />
                    <VsCalendar size={18} class={classes.calendarIcon} />
                </div>
            </div>
            <div class={classes.field}>
                <label class={classes.label}>Номер заказа</label>
                <input
                    type="text"
                    class={classes.input}
                    value={orderNumber()}
                    onInput={(e) => setOrderNumber(e.target.value)}
                    placeholder="НФХХХ"
                />
            </div>
            <div class={classes.field}>
                <label class={classes.label}>Исполнитель</label>
                <input
                    type="text"
                    class={classes.input}
                    value={executor()}
                    onInput={(e) => setExecutor(e.target.value)}
                    placeholder="ООО 'Трави Технолоджи'"
                />
            </div>
            <div class={classes.field}>
                <label class={classes.label}>Заказчик</label>
                <input
                    type="text"
                    class={classes.input}
                    value={customer()}
                    onInput={(e) => setCustomer(e.target.value)}
                    placeholder="ООО 'Аниме'"
                />
            </div>
            <div class={classes.field}>
                <label class={classes.label}>НДС</label>
                <input
                    type="text"
                    class={classes.input}
                    value={vat()}
                    onInput={(e) => setVat(e.target.value)}
                    placeholder="5%"
                />
            </div>
        </div>
    );
}