# Changelog

## [1.2.1](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.2.0...v1.2.1) (2025-01-26)


### Bug Fixes

* Update release-please configuration and workflow ([7095242](https://github.com/iamkrish-coder/IntelliTrader/commit/7095242591d0653689145c79f38b555f38687946))

## [1.2.0](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.5...v1.2.0) (2025-01-26)


### Features

* Implement password reset and forgot password functionality ([573a313](https://github.com/iamkrish-coder/IntelliTrader/commit/573a3134daf3b36891e7dc12a2e646c0a87a0d23))

## [1.1.5](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.4...v1.1.5) (2025-01-25)


### Bug Fixes

* Implement password-based authentication with credentials provider ([bf6c414](https://github.com/iamkrish-coder/IntelliTrader/commit/bf6c4144cb51db305dd2cd206636394e556878b5))

## [1.1.4](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.3...v1.1.4) (2025-01-24)


### Bug Fixes

* enhance email login using magic links ([d535fc6](https://github.com/iamkrish-coder/IntelliTrader/commit/d535fc6707979cd3d0edc6614a61de8aa5a2ffde))

## [1.1.3](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.2...v1.1.3) (2025-01-22)


### Bug Fixes

* Prevent the workflow from running on release PRs created by the bot ([0708d9d](https://github.com/iamkrish-coder/IntelliTrader/commit/0708d9df2ac4f3274a52d5269bf9d9d2fecdb721))

## [1.1.2](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.1...v1.1.2) (2025-01-22)


### Bug Fixes

* updated github workflow to run only on feature branches ([eaecf88](https://github.com/iamkrish-coder/IntelliTrader/commit/eaecf88d8af589a8e5bdd5299befdadb352857f8))

## [1.1.1](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.1.0...v1.1.1) (2025-01-22)


### Bug Fixes

* modified github workflow to create and run releases only on feature branch ([157e8f9](https://github.com/iamkrish-coder/IntelliTrader/commit/157e8f9a5ffc9cd90b58595489386c7d6cfa0b8a))
* new workflow action for releases ([1f184b8](https://github.com/iamkrish-coder/IntelliTrader/commit/1f184b81cab0daa753cdde89a2cd398ba3bc5a50))
* Update Github workflow for releases ([0cc7079](https://github.com/iamkrish-coder/IntelliTrader/commit/0cc7079f5752ef002ddd40f469f506a62cbbb2f2))
* workflow github ([ba492de](https://github.com/iamkrish-coder/IntelliTrader/commit/ba492de9356fcf6bcb41a7ef80f41c577e322bf2))

## [1.1.0](https://github.com/iamkrish-coder/IntelliTrader/compare/v1.0.0...v1.1.0) (2025-01-22)


### Features

* **auth:** implement NextAuth v5 email authentication ([bfcdb4f](https://github.com/iamkrish-coder/IntelliTrader/commit/bfcdb4ffb68dacfcb589929080dfb5d8aeb6ea7e))

## 1.0.0 (2025-01-11)


### ⚠ BREAKING CHANGES

* Refactored backend and frontend source code
* Added admin dashboard for managing frontend
* feat! add ability to add stock and index options to basket for Options Trading
* Breaking changes, introducing Market and Limit Order placement, revamped configurations, updated enum usage
* Refactored action controller to more meaningful signal processor
* Complete rewrite of application App Start modules, Async Multi Processing, significant improvement in performance, versatile logging functionalities, moved directory structures for better management of files, reduced technical debt and improved dynamic processing

### Features

* add option trading order placement and saving order to table ([9e61a78](https://github.com/iamkrish-coder/IntelliTrader/commit/9e61a78abd21640e26e897edd69b7d9cc304f88b))
* add scheduler for Strategy always running mode, 3 types of scheduler modes added ([e005b24](https://github.com/iamkrish-coder/IntelliTrader/commit/e005b246e5c01538350b7f37629effad9d47028f))
* Added a landing page, login and signup page UI ([d05d9bb](https://github.com/iamkrish-coder/IntelliTrader/commit/d05d9bb5b1f65e39908f84b42ef20edd82e26c53))
* Added admin dashboard for managing frontend ([3b0fcad](https://github.com/iamkrish-coder/IntelliTrader/commit/3b0fcadf1846d1b479d5084786d6bbec912a4fbf))
* added AWS Dynamo DB for storage, added controllers for database operations, updated logs to log database messages, refacotored aws publisher and subscriber programs ([ca1e61a](https://github.com/iamkrish-coder/IntelliTrader/commit/ca1e61a92fcbc933c0c1015cb8820ac8b348caa3))
* added caching and ability to get and put items from aws dynamo db, Topics saved to aws dynamodb ([6648ae5](https://github.com/iamkrish-coder/IntelliTrader/commit/6648ae53511e302b706c3d4a6d0d8edea8e85ef8))
* Added frontend assets from scratch. ([e5a6952](https://github.com/iamkrish-coder/IntelliTrader/commit/e5a6952d8aad0c1d1e007bc8700cd685b36d9930))
* Added Home Page, Login Page, Signup Page, Page Not Found Page ([fc55872](https://github.com/iamkrish-coder/IntelliTrader/commit/fc558728878a9efbd609f45b59a2e911ef98c14b))
* Added Initial changes for Header, fixed logout and token storage for authorization, fixed skin mode toggle and navigation menu ([34e5ebc](https://github.com/iamkrish-coder/IntelliTrader/commit/34e5ebc3fe1ca44e9c1cb1d5eb7ebb0574a749fc))
* Added login, registration and forgot password feature with improved response and exception management ([068ded2](https://github.com/iamkrish-coder/IntelliTrader/commit/068ded22d2a423aaa5caf267da85525aa3e7be83))
* added pr autiomation ([027cc9f](https://github.com/iamkrish-coder/IntelliTrader/commit/027cc9f2093e56e8e3b8d1c6251b0255c37f15f0))
* Added react to the project for Frontend development ([25c236f](https://github.com/iamkrish-coder/IntelliTrader/commit/25c236fa768f733f78642f3759732171b4c2a13d))
* Added the ability to store signals into a table for further order processing ([3cb6e91](https://github.com/iamkrish-coder/IntelliTrader/commit/3cb6e9129c47112c8724265aef82d738c54ce35c))
* Added the ability to store signals into a table for further order processing ([7d5eaa7](https://github.com/iamkrish-coder/IntelliTrader/commit/7d5eaa7a7de909a43e92198cefa9f765c9977d1a))
* Added Trade Controller - retrieves the signals from database and updates them on processing, refactored file and controller names ([88a1ac0](https://github.com/iamkrish-coder/IntelliTrader/commit/88a1ac0b479e792a0bfef756a6140e05821d6161))
* Breaking changes, introducing Market and Limit Order placement, revamped configurations, updated enum usage ([84cea47](https://github.com/iamkrish-coder/IntelliTrader/commit/84cea47cbfac7c66bea262e099c92d8061c20754))
* Complete rewrite of application App Start modules, Async Multi Processing, significant improvement in performance, versatile logging functionalities, moved directory structures for better management of files, reduced technical debt and improved dynamic processing ([ca4ef32](https://github.com/iamkrish-coder/IntelliTrader/commit/ca4ef320665a59759e937b397b270df5b2ac3797))
* database changes, needs further refactoring. Lot of changes done to the framework code ([991b332](https://github.com/iamkrish-coder/IntelliTrader/commit/991b332da67313695f338cdf53f67c0dd5140ccf))
* feat! add ability to add stock and index options to basket for Options Trading ([9b01287](https://github.com/iamkrish-coder/IntelliTrader/commit/9b01287a1d833377a7c35104090bf60c11339d22))
* fix the strategy class and async processing, also reintroducing updated actions ([8a1d5a0](https://github.com/iamkrish-coder/IntelliTrader/commit/8a1d5a0a3ba4e3eb2e8c3cee2415b34aadaaa5c7))
* fix the title of release builds ([7765c01](https://github.com/iamkrish-coder/IntelliTrader/commit/7765c0165cc423b688124d3c5f7b9cb0c616a080))
* Implement Secondary Checks before processing alerts for Buy Sell signal ([aa4b9e8](https://github.com/iamkrish-coder/IntelliTrader/commit/aa4b9e8af8a038e2ebd0dcbbcc3fa6db80ab9621))
* Implemented auto cancelling of pending and open orders after a ageing period of 5minutes ([cc53fe2](https://github.com/iamkrish-coder/IntelliTrader/commit/cc53fe21751ee47049c01b29339e9729fa207d63))
* Implemented caching to disk for larger timeframe [#293](https://github.com/iamkrish-coder/IntelliTrader/issues/293) ([d97b418](https://github.com/iamkrish-coder/IntelliTrader/commit/d97b418e9af0a1dc85a1b37af60471bfac2607f2))
* Implemented User Registration ([33d77fb](https://github.com/iamkrish-coder/IntelliTrader/commit/33d77fb7b9a6c4c1c64e79440aa34260bdca52ed))
* improved release please with configurations ([7484719](https://github.com/iamkrish-coder/IntelliTrader/commit/74847197f4fc8102f86c1eba96b654eb6ea2ad6b))
* Improved SNS Class managment, split all SNS actions to their own implmenting classes ([f0bf226](https://github.com/iamkrish-coder/IntelliTrader/commit/f0bf2268e0f8e00300d4ef6cb3666523956ee3ca))
* Improved the configuration parameter parsing to be more dynamic, fixed issues with publishing and subscribing the topic and queues, fixed the action initialization throwing async None Type error upon execution. ([1f2a51b](https://github.com/iamkrish-coder/IntelliTrader/commit/1f2a51be396d8fd7c38b2be95d45d9b3fcd9255a))
* Load and Parse Dynamic strategy using configuration files ([bd019a1](https://github.com/iamkrish-coder/IntelliTrader/commit/bd019a162c83bb58a3c395b78ffea36edc5f496d))
* Major refactoring for logging, also completed all functions within SNS operations. ([39f4d0c](https://github.com/iamkrish-coder/IntelliTrader/commit/39f4d0ca501c88e5a5bd2966384362e780b6989f))
* major refactoring, clean up, improve import and formatting ([0d9a937](https://github.com/iamkrish-coder/IntelliTrader/commit/0d9a93722f935533b11438a7e6e5435e64d61f54))
* Migrating DB from Dynamo DB to PostgreSQL ([1fa0c07](https://github.com/iamkrish-coder/IntelliTrader/commit/1fa0c07d526e1221603c122f710abcc9743be8ce))
* Modified Strategy module and Database Module to be independent ([a558964](https://github.com/iamkrish-coder/IntelliTrader/commit/a5589645677e93ebeb074acb95a61856509ac654))
* new actions workflo ([9068333](https://github.com/iamkrish-coder/IntelliTrader/commit/90683333e6c9a7b5bb4ddf00d4fa368528f1c076))
* offline api access, when subscription is not active ([13d6595](https://github.com/iamkrish-coder/IntelliTrader/commit/13d6595eb5023f05eff6cb422ff65751d3068a38))
* Password Reset Feature added ([d7fd76c](https://github.com/iamkrish-coder/IntelliTrader/commit/d7fd76cdeee96fa976b33e580d5354794d49bd3a))
* Reduce historical data request api calls ([7724a28](https://github.com/iamkrish-coder/IntelliTrader/commit/7724a28026bd83d0b6fdbc34bfb429dede501184))
* Refactor code and update TODO ([695b882](https://github.com/iamkrish-coder/IntelliTrader/commit/695b8827ae74fc7716213a972cd411da36dbb844))
* Refactored backend and frontend source code ([11adcb7](https://github.com/iamkrish-coder/IntelliTrader/commit/11adcb7aa092ea132033a4085519a460bbf39d6f))
* revised database code, dynamodb functions implemented to retrieve data, fixed cache issues of candlesticks, improved logging ([94b381f](https://github.com/iamkrish-coder/IntelliTrader/commit/94b381f6a2f89e09187f79cda96ea45c35b1f86c))
* save trades to database ([78654dc](https://github.com/iamkrish-coder/IntelliTrader/commit/78654dccf05368c91faf967e76b67f316bce0665))
* setup SNS to SQS fanout, now messages published to SNS topics are fan out to SQS queue ([08f3c1c](https://github.com/iamkrish-coder/IntelliTrader/commit/08f3c1cf3ee5e709df52f345091974a2d5181750))
* Stable Build ([53a9fa8](https://github.com/iamkrish-coder/IntelliTrader/commit/53a9fa884c328689492af83122252471473a47bf))
* Strategies and Topics Prefill and management ([cb97a98](https://github.com/iamkrish-coder/IntelliTrader/commit/cb97a98c1901caa09b6512482c2aa3f67279a599))
* updated actions ([0ecabe0](https://github.com/iamkrish-coder/IntelliTrader/commit/0ecabe03a6bb930c393f4cdb657e05c5abd6b23d))
* updated base branch in actions file ([1c9f4be](https://github.com/iamkrish-coder/IntelliTrader/commit/1c9f4beb7e90f2494261f1e5a1ba67f867788f68))
* updated database queries, refactored caching utils, connection modules, moved configurations outside modules directory ([b9e3f78](https://github.com/iamkrish-coder/IntelliTrader/commit/b9e3f788afaa6dcb1a137e1f173ea80ae49f7161))


### Bug Fixes

* Action alerts Processing and saving the watchlist of alerts ([41d0bbe](https://github.com/iamkrish-coder/IntelliTrader/commit/41d0bbe723ccbb7450d994db1aa1a01c4c147684))
* actions updated ([7f75a08](https://github.com/iamkrish-coder/IntelliTrader/commit/7f75a08c6dda7d5532519df04634921c395d1081))
* actions workflow changes ([eaa1511](https://github.com/iamkrish-coder/IntelliTrader/commit/eaa151192e1920cafd0847794818f7ba0f3657c0))
* add auto merge label ([5410a1e](https://github.com/iamkrish-coder/IntelliTrader/commit/5410a1e27d9071c57b0a953cfbc85adddf62c0de))
* add auto merge to PRs of develop branch ([e2f4cea](https://github.com/iamkrish-coder/IntelliTrader/commit/e2f4ceae39b17fd7176b16d4863f871123f23f00))
* add one more manifest configuration for release please ([e871fa2](https://github.com/iamkrish-coder/IntelliTrader/commit/e871fa2e7ee26982cc0ce57c40eaee3ddc62d558))
* added more PR automations ([a64aebd](https://github.com/iamkrish-coder/IntelliTrader/commit/a64aebd2a52dd7ed28cbfa450e250c9929a71c0b))
* added more PR automations ([5a14e1c](https://github.com/iamkrish-coder/IntelliTrader/commit/5a14e1cd7cce1ab69782f57463c2ffca7e6ecc10))
* added new action workflow ([89c248d](https://github.com/iamkrish-coder/IntelliTrader/commit/89c248d02af03ac876baa064e2afaa6870e0cfe0))
* added new CI/CD function ([41bca80](https://github.com/iamkrish-coder/IntelliTrader/commit/41bca808a9c35d7c865c6bad7c386df5e61f219d))
* added squash back ([677ec71](https://github.com/iamkrish-coder/IntelliTrader/commit/677ec71289c786ee040d9d41ef5d4b08502ab285))
* added squash back ([#250](https://github.com/iamkrish-coder/IntelliTrader/issues/250)) ([d764817](https://github.com/iamkrish-coder/IntelliTrader/commit/d764817ce41c3663302ec24e611e4e617fa672e4))
* added stored procedures and functions for database access ([28dd01d](https://github.com/iamkrish-coder/IntelliTrader/commit/28dd01dc1a1216a454f556e67d4acf82b5f31b62))
* auto create prs ([0c276f7](https://github.com/iamkrish-coder/IntelliTrader/commit/0c276f742f75b64f9248b64d95ac50fe237a6038))
* auto labels on merge updated ([5d70984](https://github.com/iamkrish-coder/IntelliTrader/commit/5d70984a331e24db0dab0c74ebe3e50f22c22b0f))
* auto merge build ([36db561](https://github.com/iamkrish-coder/IntelliTrader/commit/36db561e7b3069e7f4137d30ac457c1c05fe313d))
* auto merge changes ([39b6571](https://github.com/iamkrish-coder/IntelliTrader/commit/39b657164cd2bf7f9e575be4f823e1a0471cf4f2))
* auto PR and auto release fixes to automate CI ([21b3a91](https://github.com/iamkrish-coder/IntelliTrader/commit/21b3a911932f964cdc166192351b3d98af54ac22))
* auto PR and auto release fixes to automate CI ([f850941](https://github.com/iamkrish-coder/IntelliTrader/commit/f850941d2b1c3c1de4ce05a8e8b6fa60cb1a7fa9))
* auto relase on close ([1e0acc1](https://github.com/iamkrish-coder/IntelliTrader/commit/1e0acc16bf9998d2a4c869fdfaa9ab7ccff000d1))
* auto relase on close ([#263](https://github.com/iamkrish-coder/IntelliTrader/issues/263)) ([2ce68c6](https://github.com/iamkrish-coder/IntelliTrader/commit/2ce68c677b460b9972280a49f061badfdfe2b01a))
* auto release changes ([dd4502e](https://github.com/iamkrish-coder/IntelliTrader/commit/dd4502ec659f6fb9746fc3c680372a55eec2812a))
* auto release changes ([#265](https://github.com/iamkrish-coder/IntelliTrader/issues/265)) ([e136444](https://github.com/iamkrish-coder/IntelliTrader/commit/e136444138deba59598ea9ffb7a11d4a4162cf01))
* auto release minimal ([e272552](https://github.com/iamkrish-coder/IntelliTrader/commit/e272552a63d881edd4d2d67c637cd67290ebfce3))
* auto update config for tables when a table is deleted ([976af32](https://github.com/iamkrish-coder/IntelliTrader/commit/976af32aa8b6e24890fcfe731e62ddf390f22733))
* AWS Subscriber can now receive messages and other minor enhancements ([d7df6ff](https://github.com/iamkrish-coder/IntelliTrader/commit/d7df6ff01e4b619718225c641448d12a1c9265ff))
* change develop ([5d993bf](https://github.com/iamkrish-coder/IntelliTrader/commit/5d993bfaabf4cc8d238d867bf2611081df4d4a1a))
* ci/cd ([1893c60](https://github.com/iamkrish-coder/IntelliTrader/commit/1893c6053703e0b5e8dab6637607b7b8b219cb18))
* code changes to actions file ([5d1ffff](https://github.com/iamkrish-coder/IntelliTrader/commit/5d1ffff2faefdbcc403436cab16d6e6bef97201e))
* Create action for auto create pr ([08cb654](https://github.com/iamkrish-coder/IntelliTrader/commit/08cb6543f859b5394257e947a7a7692060ea53e2))
* create pr automatically ([61d30a1](https://github.com/iamkrish-coder/IntelliTrader/commit/61d30a111ebf5cb9f00104041cd992ad02d3b040))
* create table changes to adapt to boto3, integrated the aws sdk api call directly from the database create table class ([118b0e5](https://github.com/iamkrish-coder/IntelliTrader/commit/118b0e5169b0fbcb48e54c75b8a484873ae79f46))
* Fix parsing issues with candle data not showing index correctly ([6df6a82](https://github.com/iamkrish-coder/IntelliTrader/commit/6df6a828a55e925fc772f070df1df4cc7e2f54c4))
* formatting changes ([d0a0550](https://github.com/iamkrish-coder/IntelliTrader/commit/d0a0550a11bc170021a58d71f177081a042f0b3d))
* formatting changes ([#240](https://github.com/iamkrish-coder/IntelliTrader/issues/240)) ([ff9ed1d](https://github.com/iamkrish-coder/IntelliTrader/commit/ff9ed1dfe30b5e53d791633ca40091b675d1d639))
* improved landing page ([004d800](https://github.com/iamkrish-coder/IntelliTrader/commit/004d800a39069880879bc9ec679a33c306582bee))
* integrate boto3 into delete table module ([b0e6a97](https://github.com/iamkrish-coder/IntelliTrader/commit/b0e6a97d88b7cf01b592fd7d9520154d0602e972))
* landing page added using react and vendor assets ([96cd5d6](https://github.com/iamkrish-coder/IntelliTrader/commit/96cd5d6479aca7b97c793637eb5a0c0a2a68192d))
* method changed from squash to merge ([39311d5](https://github.com/iamkrish-coder/IntelliTrader/commit/39311d5c8746f7184e6b8553c221e2ba7636429f))
* minor fixes to logging messages and fix a bug while checking for table existence ([4a925ae](https://github.com/iamkrish-coder/IntelliTrader/commit/4a925ae88fa957a720327f22d8713a4f795b5975))
* modified publisher code to be more consistent for both Queue and Topics ([55bf705](https://github.com/iamkrish-coder/IntelliTrader/commit/55bf705e03267ad5670e703a2a9e8b97065aece8))
* Modified UI to keep required views and removed unnecessary elements ([c77523d](https://github.com/iamkrish-coder/IntelliTrader/commit/c77523d3bfdf34d097c143c1b8ff9bf4e6ae3a1f))
* Modify Auto PR actions ([20c6246](https://github.com/iamkrish-coder/IntelliTrader/commit/20c62468fb89c6dda60117906c094c145b6c1873))
* new auto pr creation action ([a5d1144](https://github.com/iamkrish-coder/IntelliTrader/commit/a5d11440377ab08ad3bb4b5a0d4ab97ce963b603))
* new patch ([8212be5](https://github.com/iamkrish-coder/IntelliTrader/commit/8212be5ac6d02fe95beed8e4a03fd8490ed6768e))
* new patch ([b8b6985](https://github.com/iamkrish-coder/IntelliTrader/commit/b8b69859291f64ed5cb2126871b80881b5618e54))
* new pathces ([3934b06](https://github.com/iamkrish-coder/IntelliTrader/commit/3934b06e656d9f59510e263ffae2e3a9544e56e7))
* nightly build 3.12.2 ([6be4a44](https://github.com/iamkrish-coder/IntelliTrader/commit/6be4a4412f34d2acb0aeef665ee5cb49f4d1c6b8))
* nightly build 3.12.3, Added access policies, SNS Topic registration improvements ([71a5e6c](https://github.com/iamkrish-coder/IntelliTrader/commit/71a5e6c9ee60a1e6bd6f8a6b69a9f48700aef07a))
* Password reset  functionality added ([32c147b](https://github.com/iamkrish-coder/IntelliTrader/commit/32c147bb275dc5fd7403afcecaf976d820fc677e))
* PAT created, action file should work now ([a036c4b](https://github.com/iamkrish-coder/IntelliTrader/commit/a036c4bfa7f532e7eb959e47cf59f0deb7899441))
* pr auto merging testing ([8e1e8cd](https://github.com/iamkrish-coder/IntelliTrader/commit/8e1e8cd30799ba82efc266318f1fa71e8244853a))
* prepare frontend project package for development ([b40d4c8](https://github.com/iamkrish-coder/IntelliTrader/commit/b40d4c8c030b31d4035b18dbfc3db223eb76f3c8))
* prepare frontend project package for development ([d7d8330](https://github.com/iamkrish-coder/IntelliTrader/commit/d7d8330178777b3a8d10ce55f226631bf5dc9cf4))
* rebase to squash ([d1491f6](https://github.com/iamkrish-coder/IntelliTrader/commit/d1491f67de5738e870bd377e21af21380fe7b660))
* refactored controllers ([cd8606f](https://github.com/iamkrish-coder/IntelliTrader/commit/cd8606f65ccb396b15778767fc0a9792771e0b31))
* refactored publisher and database code to ([98752c0](https://github.com/iamkrish-coder/IntelliTrader/commit/98752c0221f40cbe6670e0dad7504f00ae801c86))
* release automation workflow and configuration files ([8442dfa](https://github.com/iamkrish-coder/IntelliTrader/commit/8442dfa3c1aa1b21a4768928416d614c50ace1ad))
* Remove actions ([81ba892](https://github.com/iamkrish-coder/IntelliTrader/commit/81ba892a04a93151d7933d77d89a00b992c2426e))
* remove an actions workflow which is unnecessary ([22c95b4](https://github.com/iamkrish-coder/IntelliTrader/commit/22c95b49e7df14f36dece413b5756f0cb323e865))
* remove auto PR for one last time, let us focus on priorities ([f862b78](https://github.com/iamkrish-coder/IntelliTrader/commit/f862b784565ff1be9e3e0d76da76f6b13f8e4abc))
* remove check for changes ([50294f6](https://github.com/iamkrish-coder/IntelliTrader/commit/50294f655017bd6c48963f6edc134b00ab6b3ddf))
* remove keyboard package from project, no longer in use ([7dd2d99](https://github.com/iamkrish-coder/IntelliTrader/commit/7dd2d993da891fddbb3410e571861c1ff375e90a))
* remove refs on master ([3c46d66](https://github.com/iamkrish-coder/IntelliTrader/commit/3c46d66acbc4c181ac33a4e49baa2123ba7a84a5))
* remove unwanted cache file creation, fix the list error, remove comparison operator file ([848c6aa](https://github.com/iamkrish-coder/IntelliTrader/commit/848c6aa66814f3710c20c7f7b8d44774d76e1513))
* removed residual files ([91ae3d5](https://github.com/iamkrish-coder/IntelliTrader/commit/91ae3d54dfda65c3eee592df14aa38450a71a329))
* Renamed files ([e5390f3](https://github.com/iamkrish-coder/IntelliTrader/commit/e5390f354dbc2d94ff6c8582342622fd2d5c52cb))
* Renamed files for consistent naming conventions ([343681f](https://github.com/iamkrish-coder/IntelliTrader/commit/343681fb5744ba1fd0612ae24d960fbe79e32ecf))
* resolve conflicts ([90b30ab](https://github.com/iamkrish-coder/IntelliTrader/commit/90b30ab43b00b11f50b885670c63c143eb5388e6))
* run auto release every hour ([724879c](https://github.com/iamkrish-coder/IntelliTrader/commit/724879cbc5f0942f4292c5503a15d20f3dbda07e))
* run auto release every hour ([#262](https://github.com/iamkrish-coder/IntelliTrader/issues/262)) ([f408c5f](https://github.com/iamkrish-coder/IntelliTrader/commit/f408c5f5366e6d241378f1f3d31bcf666f483d5c))
* SNS and SQS Fan out of stock alerts published, minor fixes and enhancements ([3678c11](https://github.com/iamkrish-coder/IntelliTrader/commit/3678c11f58694c4aafe735b4c8c8517190b549bf))
* spaces used in actions ([0284fc5](https://github.com/iamkrish-coder/IntelliTrader/commit/0284fc557f97c94d9505d0f488f286b7d4c8c235))
* Testing new pr creation ([af7491d](https://github.com/iamkrish-coder/IntelliTrader/commit/af7491d341face7ad5521ffef97810416cceaca6))
* testing out older changes for actions ([77c4416](https://github.com/iamkrish-coder/IntelliTrader/commit/77c44169bdb5bd5119871dcaae544250ae4c10bb))
* Update branch name convention for releaseplease ([f5a12b4](https://github.com/iamkrish-coder/IntelliTrader/commit/f5a12b47c34e945d5f414581e2ac951e61d057a2))
* update pyproj files ([003eb07](https://github.com/iamkrish-coder/IntelliTrader/commit/003eb073c1f09eb8b3086710608d34c3f28b44d6))
* Update releae please to auto merge ([ce79de2](https://github.com/iamkrish-coder/IntelliTrader/commit/ce79de27b5246b24c3e5519ad1616944fed9f9ea))
* Update release workflow and remove verification_token table ([cefec67](https://github.com/iamkrish-coder/IntelliTrader/commit/cefec67b9a9ca92cc2dcd2afd0c5607592124e7d))
* update timeframe text in console output ([ab2928c](https://github.com/iamkrish-coder/IntelliTrader/commit/ab2928ca1703e57db64282901e60718de1f9d5de))
* Update title of release ([e84eca6](https://github.com/iamkrish-coder/IntelliTrader/commit/e84eca634f4eab22159084c1a05ef1b66ceafc37))
* update to auto merge v12 ([8341cd4](https://github.com/iamkrish-coder/IntelliTrader/commit/8341cd40b489efa57e22314ae1f666abd50230bc))
* update to auto merge v12 ([2bc8838](https://github.com/iamkrish-coder/IntelliTrader/commit/2bc8838e679e3c0e762341126b3f6ab0bb72ebad))
* Update version in release-please-manifest.json to 8.7.0 ([dddd166](https://github.com/iamkrish-coder/IntelliTrader/commit/dddd1669d8a7cbdadcb470213125bdf4087088da))
* Update version in release-please-manifest.json to 8.7.0 ([f501de8](https://github.com/iamkrish-coder/IntelliTrader/commit/f501de8237151b49b644bc8741dcfc4d173893de))
* Update version in release-please-manifest.json to 8.7.0 ([a71920f](https://github.com/iamkrish-coder/IntelliTrader/commit/a71920f37bbee499fd72cdd9bdddc267e5749528))
* updated actions file changes ([e9b3b2b](https://github.com/iamkrish-coder/IntelliTrader/commit/e9b3b2b3dd21b726396cd8f2fc86e19ac4426dc3))
* updated actions to sync release and master  every x mins ([8c24f75](https://github.com/iamkrish-coder/IntelliTrader/commit/8c24f75728daa00b95a97c70da6c127105c3f10c))
* updated actions workflow to sync the changes back to develop ([9f7666a](https://github.com/iamkrish-coder/IntelliTrader/commit/9f7666a72736cb51a33673ea081b1149cbfa1bd3))
* updated changes for actions ([b469224](https://github.com/iamkrish-coder/IntelliTrader/commit/b469224a28a448fdb7a566a856754e9c9d55181a))
* Updated css ([d62d69e](https://github.com/iamkrish-coder/IntelliTrader/commit/d62d69e55bcb275519eb8bb5e56614e948a45cf5))
* updated labels ([5d6c882](https://github.com/iamkrish-coder/IntelliTrader/commit/5d6c882af67862acb312ebd0c3329951a98cdd76))
* updated labels ([a00615d](https://github.com/iamkrish-coder/IntelliTrader/commit/a00615ddb2441e09a59e3395c1da899ab1622b5e))
* updated login and registration pages with react form validations ([ace8a5b](https://github.com/iamkrish-coder/IntelliTrader/commit/ace8a5b8e9c41e8fc15699d69f3bfc2574b86b75))
* updated menu and header ([a0c3b97](https://github.com/iamkrish-coder/IntelliTrader/commit/a0c3b9771b0bc90c49c0d307afa39f121bcd5cd9))
* updated python version ([cfe7c00](https://github.com/iamkrish-coder/IntelliTrader/commit/cfe7c0040a3bd20d2fc41559222a854dcefa56f2))
* Updated release please ([d2f716d](https://github.com/iamkrish-coder/IntelliTrader/commit/d2f716d20c9c42ce641ee9da3d7ca4cca3772178))
* Updated Strategy Parsing techniques to be more structured and robust ([6b4e588](https://github.com/iamkrish-coder/IntelliTrader/commit/6b4e58821d497ae1ac89176782628f8a6bf901f1))
* Updated Strategy Parsing techniques to be more structured and robust ([f1f9d2c](https://github.com/iamkrish-coder/IntelliTrader/commit/f1f9d2c1a50e0041588e8ce1e9ac6fa2cb655381))
* updated the menu and sidebar for the dashboard view ([b5d2efe](https://github.com/iamkrish-coder/IntelliTrader/commit/b5d2efee3c9b675302e1eb0f542c7cd6e20f4e91))
* updated to use peter evans create pull request action ([10e8d13](https://github.com/iamkrish-coder/IntelliTrader/commit/10e8d13b409f2884719c6a124f4fc3cb0c3cc9d4))


### Code Refactoring

* Refactored action controller to more meaningful signal processor ([bc78651](https://github.com/iamkrish-coder/IntelliTrader/commit/bc78651206a1dea1560a980da04851155e3436f9))
