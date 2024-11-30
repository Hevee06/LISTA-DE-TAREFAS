document.addEventListener("DOMContentLoaded", function() {
    const tarefaList = document.getElementById("tarefa-list");

    new Sortable(tarefaList, {
        animation: 150,
        onEnd(evt) {
            const orderedTarefas = Array.from(tarefaList.children).map((item, index) => {
                return {
                    id: item.dataset.id,
                    ordem: index + 1
                };
            });

            fetch("/reorder", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ tarefas: orderedTarefas })
            }).then(response => {
                if (response.ok) {
                    console.log('Tarefas reordenadas com sucesso!');
                } else {
                    console.log('Erro ao reordenar tarefas.');
                }
            });
        }
    });
});
