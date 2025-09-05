// Quick game availability test script
// Run this in browser console on http://localhost:3000/game-availability-test.html

function quickTest() {
    console.log('🚀 Starting quick game test...');
    
    // Key games to test (high-priority ones we replaced)
    const testGames = [
        { id: 'tetris-classic', title: 'Tetris', url: 'https://poki.com/en/g/tetris' },
        { id: '2048-game', title: '2048', url: 'https://2048game.com/' },
        { id: 'chess-online', title: 'Chess', url: 'https://lichess.org/' },
        { id: 'sudoku-puzzle', title: 'Sudoku', url: 'https://poki.com/en/g/sudoku-village' },
        { id: 'bubble-shooter', title: 'Bubble Shooter', url: 'https://bubbleshooter.net/' }
    ];
    
    let results = { success: 0, failed: 0, total: testGames.length };
    
    testGames.forEach((game, index) => {
        setTimeout(() => {
            console.log(`Testing ${game.title}...`);
            
            const iframe = document.createElement('iframe');
            iframe.style.width = '300px';
            iframe.style.height = '200px';
            iframe.style.border = '1px solid #ccc';
            iframe.style.margin = '10px';
            
            let loadTimer = setTimeout(() => {
                console.log(`❌ ${game.title} - Timeout`);
                results.failed++;
                checkComplete();
            }, 8000);
            
            iframe.onload = () => {
                console.log(`✅ ${game.title} - Loaded successfully`);
                clearTimeout(loadTimer);
                results.success++;
                checkComplete();
            };
            
            iframe.onerror = () => {
                console.log(`❌ ${game.title} - Load error`);
                clearTimeout(loadTimer);
                results.failed++;
                checkComplete();
            };
            
            iframe.src = game.url;
            document.body.appendChild(iframe);
            
            function checkComplete() {
                if (results.success + results.failed === results.total) {
                    console.log('\n🎯 Test Complete!');
                    console.log(`✅ Success: ${results.success}/${results.total} (${Math.round(results.success/results.total*100)}%)`);
                    console.log(`❌ Failed: ${results.failed}/${results.total} (${Math.round(results.failed/results.total*100)}%)`);
                }
            }
            
        }, index * 1000);
    });
}

// Auto-run when script loads
console.log('Game test script loaded. Run quickTest() to start testing.');