let currentPage = 1;
let isLoading = false;
let hasNextPage = true;
let myRankValue = null;

const myRankRow = document.getElementById("my-rank-row");
const myRankWrapper = document.getElementById("my-rank-wrapper");
const tbody = document.getElementById("leaderboard-body");
const loader = document.getElementById("leaderboard-loader");
const sentinel = document.getElementById("leaderboard-sentinel");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function loadLeaderboardPage() {
    if (isLoading || !hasNextPage) return;

    isLoading = true;
    loader?.classList.remove("hidden");

    try {
        await sleep(1000);

        const response = await fetch(`/api/leaderboard/?page=${currentPage}`);
        if (!response.ok) throw new Error("Failed to load leaderboard");

        const data = await response.json();

        if (currentPage === 1 && data.my_rank) {
            myRankValue = data.my_rank.rank;
            renderMyRank(data.my_rank);
        }

        renderRows(data.results);

        hasNextPage = Boolean(data.next);
        currentPage += 1;
    } catch (error) {
        console.error(error);
    } finally {
        isLoading = false;
        loader?.classList.add("hidden");
    }
}

function renderRows(users) {
    users.forEach(user => {
        const tr = document.createElement("tr");

        if (user.rank === 1) tr.classList.add("rank-1");
        if (user.rank === 2) tr.classList.add("rank-2");
        if (user.rank === 3) tr.classList.add("rank-3");
        if (user.is_friend) tr.classList.add("friend-row");

        if (user.is_me) {
            tr.classList.add("user-row");
            myRankWrapper.classList.add("hidden");
        }

        tr.innerHTML = `
            <td>${renderRank(user.rank)}</td>
            <td>${user.personaname}</td>
            <td class="rating-high">${user.total_rating}</td>
        `;

        tbody.appendChild(tr);
    });
}

function renderRank(rank) {
    if (rank === 1) return "🥇";
    if (rank === 2) return "🥈";
    if (rank === 3) return "🥉";
    return rank;
}

function renderMyRank(user) {
    if (!user) return;

    myRankRow.innerHTML = `
        <td>${renderRank(user.rank)}</td>
        <td>${user.personaname}</td>
        <td class="rating-high">${user.total_rating}</td>
    `;

    myRankWrapper.classList.remove("hidden");
}

const observer = new IntersectionObserver(
    (entries) => {
        if (entries[0].isIntersecting) {
            loadLeaderboardPage();
        }
    },
    { rootMargin: "300px" }
);

observer.observe(sentinel);
loadLeaderboardPage();
