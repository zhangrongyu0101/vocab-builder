interface SimilarWordsData {
    words: string[];
    similarityType: string;
}

interface SimilarWordGroup {
    _id: string;
    words: string[];
    similarityType: string;
}

async function deleteWordGroup(groupId: string) {
    openModal()
    try {
        fetch(`/delete/similar-words/${groupId}`, {
            method: 'DELETE',
        });

        closeModal();
        fetchSimilarWords();
        window.location.reload(); // 强制刷新页面
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting the word group');
    }
    window.location.reload();
}


// 这个函数重新从后端加载并显示所有相似单词组
// async function fetchSimilarWords(): Promise<void> {
//     try {
//         const response = await fetch('/similar-words');
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const wordGroups: SimilarWordGroup[] = await response.json();

//         const container = getElementById<HTMLDivElement>('wordGroupsContainer');
//         container.innerHTML = ''; // 清空现有内容

//         wordGroups.forEach(group => {
//             const groupDiv = document.createElement('div');
//             groupDiv.className = 'word-group';
//             groupDiv.textContent = `Words: ${group.words.join(', ')} (Type: ${group.similarityType})`;
//             container.appendChild(groupDiv);
//         });
//     } catch (error) {
//         console.error('Error fetching similar words:', error);
//     }
// }

function fetchSimilarWords(): void {
    fetch('/similar-words')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((wordGroups: SimilarWordGroup[]) => {
            const container = getElementById<HTMLDivElement>('wordGroupsContainer');
            container.innerHTML = ''; // 清空现有内容

            wordGroups.forEach(group => {
                const groupDiv = document.createElement('div');
                groupDiv.className = 'word-group';
                groupDiv.textContent = `Words: ${group.words.join(',')} (Type: ${group.similarityType})`;
                container.appendChild(groupDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching similar words:', error);
        });
}

// 获取元素的辅助函数，增加了类型断言
function getElementById<T extends HTMLElement>(id: string): T {
    const element = document.getElementById(id);
    if (!element) throw new Error(`Element with id ${id} not found`);
    return element as T;
}

function openModal(): void {
    const modal = getElementById<HTMLDivElement>('modal');
    modal.style.display = 'block';
}

function closeModal(): void {
    const modal = getElementById<HTMLDivElement>('modal');
    modal.style.display = 'none';
}



// 绑定事件
document.addEventListener('DOMContentLoaded', () => {
    const addWordGroupBtn = getElementById<HTMLButtonElement>('addWordGroupBtn');
    addWordGroupBtn.addEventListener('click', openModal);
});
