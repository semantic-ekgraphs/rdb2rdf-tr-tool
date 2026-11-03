function StepReview({ steps, waiting, onConfirm }) {
   const [choices, setChoices] = useState(steps);

   const toggle = (i) =>
      setChoices((prev) =>
         prev.map((s, idx) =>
            idx === i
               ? { ...s, status: s.status === "enabled" ? "disabled" : "enabled" }
               : s
         )
      );

   return (
      <div>
         {choices.map((step, i) => (
            <label key={i}>
               <input
                  type="checkbox"
                  checked={step.status === "enabled"}
                  disabled={!waiting}
                  onChange={() => toggle(i)}
               />
               {step.description}
            </label>
         ))}
         <button disabled={!waiting} onClick={() => onConfirm(choices)}>
            Confirm
         </button>
      </div>
   );
}