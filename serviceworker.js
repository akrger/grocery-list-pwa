self.importScripts('static/js/sw-toolbox.js');
toolbox.precache(['static/css/style.css']);
// toolbox.router.get('*.css', toolbox.cacheOnly, {
//     cache: {
// 	name: 'csscache',
// 	maxEntries: 50,
//     },
// });

toolbox.router.get('/*', toolbox.networkFirst, {
    cache: {
	name: 'cache',
	maxEntries: 50,
    },
});
