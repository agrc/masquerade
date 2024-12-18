# Changelog

## [1.5.6-2](https://github.com/agrc/masquerade/compare/v1.5.6-1...v1.5.6-2) (2024-12-18)


### Bug Fixes

* handle non-integer maxLocations parameter ([6d69da3](https://github.com/agrc/masquerade/commit/6d69da3b33ab99fe91cd7897681740738fad5e76))

## [1.5.6-1](https://github.com/agrc/masquerade/compare/v1.5.5...v1.5.6-1) (2024-12-18)


### Bug Fixes

* clean up and add city/county to standardized address ([b8655b9](https://github.com/agrc/masquerade/commit/b8655b9df92714eb137246fe3688f84f46e59eb2))
* fix bug causing some candidates to be ignored ([ee5f7c3](https://github.com/agrc/masquerade/commit/ee5f7c39f9f69ea4e777adc66b55f58b2dc57fae))
* honor max_locations parameter for geocode requests ([b0a6069](https://github.com/agrc/masquerade/commit/b0a606946b1aefc005ba53aabfcdf154895fd44e))
* support both variations of the single line input param name ([4a552c4](https://github.com/agrc/masquerade/commit/4a552c4cdc74ed55a182db70749111f1366fd574))

## [1.5.6-0](https://github.com/agrc/masquerade/compare/v1.5.5-4...v1.5.6-0) (2024-12-18)


### Bug Fixes

* clean up and add city/county to standardized address ([dee4a30](https://github.com/agrc/masquerade/commit/dee4a303ab17bf3f2c7298d4b02246920742cf1c))
* fix bug causing some candidates to be ignored ([8af42e3](https://github.com/agrc/masquerade/commit/8af42e384a8de34fcb7fc594781de0317cf8a14b))
* honor max_locations parameter for geocode requests ([834afd3](https://github.com/agrc/masquerade/commit/834afd3f15de4f0117cfb152c79add84bd0a1a74))
* support both variations of the single line input param name ([57cb36a](https://github.com/agrc/masquerade/commit/57cb36a0e1e5fde0f6e803b97b767fbbd429360a))

## [1.5.5](https://github.com/agrc/masquerade/compare/v1.5.4...v1.5.5) (2024-12-09)


### Features

* add reverse geocoding endpoint ([b138b80](https://github.com/agrc/masquerade/commit/b138b80da2283a7d463c948d46ab87262cf76d97)), closes [#169](https://github.com/agrc/masquerade/issues/169)
* replace address grid with city/county name for geocoding results ([84038a9](https://github.com/agrc/masquerade/commit/84038a963d20533e39650beadb1b6249a62479ba)), closes [#182](https://github.com/agrc/masquerade/issues/182)


### Bug Fixes

* add types and return consistent type ([f62fc6f](https://github.com/agrc/masquerade/commit/f62fc6f6d460056e1f37bb864b07eea72b806801))
* escape returned input parameters ([2db0bb0](https://github.com/agrc/masquerade/commit/2db0bb0aeeeeae27585d24588740dbc79e675da8))
* escape while preserving numbers ([a46430a](https://github.com/agrc/masquerade/commit/a46430a2fa63830130b4b0d354f962a3eeb85f1b))
* fix duplicate "COUNTY" in reverse geocode results ([a8ac00a](https://github.com/agrc/masquerade/commit/a8ac00a7f412cbc67c7aee4462be54b241a64678))
* handle bad json parameters ([c8d1a9d](https://github.com/agrc/masquerade/commit/c8d1a9dc07894d8828bc9eb10cbfdf5dda151c1d))
* use flask logger rather than print statements ([c3e2ca0](https://github.com/agrc/masquerade/commit/c3e2ca08a41128849274874dfbf4a1731e763bd9))
* use parameterized query for user inputs ([fc06639](https://github.com/agrc/masquerade/commit/fc066398b15626fdba126ff6b66bc7b62c9200b4))


### Dependencies

* bump deps ([1ce5264](https://github.com/agrc/masquerade/commit/1ce526411e4f7f2791a813734f1ff621a086cb5b))
* python 3.10 -&gt; 3.12 and other bumps ([57b44db](https://github.com/agrc/masquerade/commit/57b44dbe9c0344239c51f9c37907e562b59843ab))

## [1.5.5-4](https://github.com/agrc/masquerade/compare/v1.5.5-3...v1.5.5-4) (2024-12-06)


### Bug Fixes

* handle bad json parameters ([7bed818](https://github.com/agrc/masquerade/commit/7bed81881dab1db8f1f30990b626abcf648ef526))

## [1.5.5-3](https://github.com/agrc/masquerade/compare/v1.5.5-2...v1.5.5-3) (2024-12-06)


### Features

* replace address grid with city/county name for geocoding results ([f7fb731](https://github.com/agrc/masquerade/commit/f7fb7317cd39cd60b8c8389b761056a47e0c2e90)), closes [#182](https://github.com/agrc/masquerade/issues/182)


### Bug Fixes

* fix duplicate "COUNTY" in reverse geocode results ([c78ae46](https://github.com/agrc/masquerade/commit/c78ae46b70e2227a306e024c16a9753722f0ce0e))

## [1.5.5-2](https://github.com/agrc/masquerade/compare/v1.5.5-1...v1.5.5-2) (2024-12-06)


### Bug Fixes

* add types and return consistent type ([76ca7f0](https://github.com/agrc/masquerade/commit/76ca7f0e3fb89feeb2642fe21ed9973f5d1c7757))
* escape returned input parameters ([f329207](https://github.com/agrc/masquerade/commit/f32920764492b37f0c63242acd543ca70b5b9291))
* escape while preserving numbers ([7bb2170](https://github.com/agrc/masquerade/commit/7bb21705053ec1bbd5724ab6f7860e754d79d535))
* use flask logger rather than print statements ([440a783](https://github.com/agrc/masquerade/commit/440a783bbaa1721281ab4970e96ae5a0a67aa2c8))
* use parameterized query for user inputs ([1ace326](https://github.com/agrc/masquerade/commit/1ace326423fd940a9c5149bf96c9271285f30425))

## [1.5.5-1](https://github.com/agrc/masquerade/compare/v1.5.4...v1.5.5-1) (2024-12-06)


### Features

* add reverse geocoding endpoint ([e4f4844](https://github.com/agrc/masquerade/commit/e4f484438d02ecb15ee37f7836107c7a69a9428e)), closes [#169](https://github.com/agrc/masquerade/issues/169)


### Dependencies

* bump deps ([1ce5264](https://github.com/agrc/masquerade/commit/1ce526411e4f7f2791a813734f1ff621a086cb5b))
* python 3.10 -&gt; 3.12 and other bumps ([dcbcbb0](https://github.com/agrc/masquerade/commit/dcbcbb03ace591e156ebb453ded235c77f98dacb))

## [1.5.5-0](https://github.com/agrc/masquerade/compare/v1.5.4...v1.5.5-0) (2024-11-27)


### Dependencies

* bump deps ([1ce5264](https://github.com/agrc/masquerade/commit/1ce526411e4f7f2791a813734f1ff621a086cb5b))

## [1.5.4](https://github.com/agrc/masquerade/compare/v1.5.3...v1.5.4) (2024-10-04)


### Dependencies

* bump the major-dependencies group across 1 directory with 2 updates ([e4e7e80](https://github.com/agrc/masquerade/commit/e4e7e8051861b702e0f090da121ddc4e2e07d0e7))

## [1.5.3](https://github.com/agrc/masquerade/compare/v1.5.2...v1.5.3) (2024-07-10)


### Dependencies

* bump ruff to latest minor ([f635186](https://github.com/agrc/masquerade/commit/f6351864f6c0e0a9f3c0c79b3cc03077be3fb167))

## [1.5.2](https://github.com/agrc/masquerade/compare/v1.5.1...v1.5.2) (2024-07-10)


### Bug Fixes

* remove ruff pytest plugin and run separately ([05a6239](https://github.com/agrc/masquerade/commit/05a62391caee5688501de0923b5a759f6a016f44))


### Dependencies

* bump the major-dependencies group across 1 directory with 3 updates ([e409da1](https://github.com/agrc/masquerade/commit/e409da1723a10a935549eb459d1ab20ddbdbd56f))


### Documentation

* point to new EB app for testing ([0382aad](https://github.com/agrc/masquerade/commit/0382aad0f7de35c847c572e98e8a65fe8401612a)), closes [#183](https://github.com/agrc/masquerade/issues/183)
* refine setup docs ([bd74313](https://github.com/agrc/masquerade/commit/bd74313595ec4bafb94355d547a05ed2e3bdf9dc))

## [1.5.1](https://github.com/agrc/masquerade/compare/v1.5.0...v1.5.1) (2024-04-15)


### 🐛 Bug Fixes

* typo ([35c9bd6](https://github.com/agrc/masquerade/commit/35c9bd608acd5cb31de6fd7dd113f23c55fb59dc))


### 🌲 Dependencies

* q4 updates ([9ef376b](https://github.com/agrc/masquerade/commit/9ef376b01dcdb2a59886880a07cbbdb12dd0d264))
* update ci deps ([cea94e8](https://github.com/agrc/masquerade/commit/cea94e80175457ed9502a6e213c93f1baadd8da4))


### 📖 Documentation Improvements

* update badge ([56ef010](https://github.com/agrc/masquerade/commit/56ef010a7f4aa83a6158bd20dbba1786a5ac2243))
* update badge ([7e00b71](https://github.com/agrc/masquerade/commit/7e00b71e9f3fdfe26896206038346d05180572a4))

## [1.5.1-0](https://github.com/agrc/masquerade/compare/v1.5.0...v1.5.1-0) (2024-04-15)


### 🐛 Bug Fixes

* typo ([35c9bd6](https://github.com/agrc/masquerade/commit/35c9bd608acd5cb31de6fd7dd113f23c55fb59dc))


### 🌲 Dependencies

* update ci deps ([a41759c](https://github.com/agrc/masquerade/commit/a41759cbb1faada9af5eedb8402e9cac81d6e9f6))

## [1.5.0](https://github.com/agrc/masquerade/compare/v1.4.1...v1.5.0) (2024-01-11)


### 🚀 Features

* add support for single-line input for batch jobs ([89793ac](https://github.com/agrc/masquerade/commit/89793acea3f78666bb3bc2cc057ec49a12c10c31))


### 🐛 Bug Fixes

* tests ([c3fdae5](https://github.com/agrc/masquerade/commit/c3fdae5e1556fccc0635e742f355dc526601a92f))

## [1.5.0-0](https://github.com/agrc/masquerade/compare/v1.4.0-0...v1.5.0-0) (2024-01-09)


### 🚀 Features

* add support for single-line input for batch jobs ([de1c9bc](https://github.com/agrc/masquerade/commit/de1c9bccb638dbc5e788d81d4ba53170220bd1aa))


### 🐛 Bug Fixes

* tests ([7a6dd04](https://github.com/agrc/masquerade/commit/7a6dd04fea9663da4eed240504c3a6501c4f4d5d))

## [1.4.1](https://github.com/agrc/masquerade/compare/v1.4.0...v1.4.1) (2024-01-08)


### 🐛 Bug Fixes

* switch back to agrc header to match other clients ([d6b5c1c](https://github.com/agrc/masquerade/commit/d6b5c1c336f15f7f44b2ceb8c368071b4aecd574))


### 🌲 Dependencies

* **dev:** bump the major-dependencies group with 1 update ([653594b](https://github.com/agrc/masquerade/commit/653594b76e697fa9317f09f114ce4569dc7270e2))

## [1.4.0](https://github.com/agrc/masquerade/compare/v1.2.2...v1.4.0) (2023-12-12)


### 🚀 Features

* add post options to the base requests as well ([2c84561](https://github.com/agrc/masquerade/commit/2c84561218d8bd364c796dd025cd477627ebc349))
* add post to allow methods for geocodeAddresses and suggest ([5ebd6f6](https://github.com/agrc/masquerade/commit/5ebd6f67557e93cb150dc8f5c4928127c60c037b))


### 🐛 Bug Fixes

* correctly get output spatial reference for POST requests ([5bf0b56](https://github.com/agrc/masquerade/commit/5bf0b561aa030a9533074ce7930ba230ad1db792))
* correctly obtain params for post requests ([f133e72](https://github.com/agrc/masquerade/commit/f133e720e62504c89bb2aa04b14e5d8931e54366))
* support requests that use url params or form data independent of the method ([1900f23](https://github.com/agrc/masquerade/commit/1900f23fe0795fe44db7853597ef2035bf3b8087))


### 🌲 Dependencies

* bump the major-dependencies group with 2 updates ([82861e6](https://github.com/agrc/masquerade/commit/82861e6a9b8f268f7b85622b1c820ca1e2af3b01))

## [1.4.0-0](https://github.com/agrc/masquerade/compare/v1.3.0-0...v1.4.0-0) (2023-12-08)


### 🚀 Features

* add post options to the base requests as well ([6a26984](https://github.com/agrc/masquerade/commit/6a269844e84ce9f3107237133cb2da206fe9b242))


### 🐛 Bug Fixes

* support requests that use url params or form data independent of the method ([4781f47](https://github.com/agrc/masquerade/commit/4781f47bae3d3b30739c8592aa4c173a170742cc))

## [1.3.0-0](https://github.com/agrc/masquerade/compare/v1.2.2...v1.3.0-0) (2023-12-08)


### 🚀 Features

* add post to allow methods for geocodeAddresses and suggest ([2c00443](https://github.com/agrc/masquerade/commit/2c00443a58dfe7f02b0df0a80e93b65aadd88833))


### 🐛 Bug Fixes

* correctly get output spatial reference for POST requests ([8467e00](https://github.com/agrc/masquerade/commit/8467e009838ac4778f2f1662befd4d1273d1b554))
* correctly obtain params for post requests ([8fa5aba](https://github.com/agrc/masquerade/commit/8fa5abacc0271f570f64e78da479441685b07ac1))


### 🌲 Dependencies

* bump the major-dependencies group with 2 updates ([cabf765](https://github.com/agrc/masquerade/commit/cabf7653a9e670921f3d25a3a8f28e5eab95b10a))

## [1.2.2](https://github.com/agrc/masquerade/compare/v1.2.1...v1.2.2) (2023-12-07)


### 🐛 Bug Fixes

* remove false advertising for reverse geocoding ([3dad698](https://github.com/agrc/masquerade/commit/3dad698b9c2b06b044b7d5fc02d7394793f47686))

## [1.2.1](https://github.com/agrc/masquerade/compare/v1.2.0...v1.2.1) (2023-10-10)


### 🌲 Dependencies

* more specific versions ([ce5902c](https://github.com/agrc/masquerade/commit/ce5902cd8d60847d7d206cb0203b65db504f0de5))

## [1.2.0](https://github.com/agrc/masquerade/compare/v1.1.12...v1.2.0) (2023-08-30)


### 🚀 Features

* show suggestions when the prefix direction is missing ([a86620f](https://github.com/agrc/masquerade/commit/a86620ff3e60f0be9ea0c148fb30869203d11083)), closes [#157](https://github.com/agrc/masquerade/issues/157)


### 🐛 Bug Fixes

* finish up agrc -&gt; ugrc ([7bc5600](https://github.com/agrc/masquerade/commit/7bc56003316fa6cf0e2162201c50c6ebf8482200))
* handle short-hand output spatial reference parameter ([d40b7b9](https://github.com/agrc/masquerade/commit/d40b7b934df8ad4718eb4bbf034f3c6d6355650f)), closes [#153](https://github.com/agrc/masquerade/issues/153)

## [1.2.0-0](https://github.com/agrc/masquerade/compare/v1.1.12...v1.2.0-0) (2023-08-29)


### 🚀 Features

* show suggestions when the prefix direction is missing ([599c32d](https://github.com/agrc/masquerade/commit/599c32dbefaa2b9f2b31ea70588ace207848aa6f)), closes [#157](https://github.com/agrc/masquerade/issues/157)


### 🐛 Bug Fixes

* finish up agrc -&gt; ugrc ([0cb3dbe](https://github.com/agrc/masquerade/commit/0cb3dbefb14771af97ed46bfb886765706df07c8))
* handle short-hand output spatial reference parameter ([250ef8d](https://github.com/agrc/masquerade/commit/250ef8de2b6261cafa78d9a94e906c325813bc5f)), closes [#153](https://github.com/agrc/masquerade/issues/153)

## [1.1.12](https://github.com/agrc/masquerade/compare/v1.1.11...v1.1.12) (2023-07-07)


### 🐛 Bug Fixes

* Q3 Dependency Bumps 🌲 ([5a5365b](https://github.com/agrc/masquerade/commit/5a5365b140ad0111cd53b0e027114967b062cd9e))
* update title so pytest picks up it's options ([58dda75](https://github.com/agrc/masquerade/commit/58dda75343a7d68909bdc2744571ef5076559ff8))


### 📖 Documentation Improvements

* AGRC -&gt; UGRC ([dfc98ae](https://github.com/agrc/masquerade/commit/dfc98aece379a0e37f015c3c5c99cf5d05a517e3))

## [1.1.12-1](https://github.com/agrc/masquerade/compare/v1.1.11...v1.1.12-1) (2023-07-03)


### 🐛 Bug Fixes

* Q3 Dependency Bumps 🌲 ([bbb31cd](https://github.com/agrc/masquerade/commit/bbb31cdb1620c4c690e48c3ce05bd944292c5f83))
* update title so pytest picks up it's options ([58dda75](https://github.com/agrc/masquerade/commit/58dda75343a7d68909bdc2744571ef5076559ff8))

## [1.1.12-0](https://github.com/agrc/masquerade/compare/v1.1.11-1...v1.1.12-0) (2023-07-03)


### 🐛 Bug Fixes

* Q3 Dependency Bumps 🌲 ([3497206](https://github.com/agrc/masquerade/commit/3497206cfe0aa2014147d25c3f0d5d80ee70114e))

## [1.1.11](https://github.com/agrc/masquerade/compare/v1.1.10...v1.1.11) (2023-06-20)


### 🐛 Bug Fixes

* handle missing keys in batch data ([301fc0b](https://github.com/agrc/masquerade/commit/301fc0ba6433dee23510e6a7cae1c1473a84e078))
* more retries on database queries with less wait ([81f0f34](https://github.com/agrc/masquerade/commit/81f0f346dbe0252a63d7f8738bee5f1f2f17e798))


### 📖 Documentation Improvements

* add time units ([f497177](https://github.com/agrc/masquerade/commit/f497177a38882e80751f2c98064b3c9504623def))
* update code coverage badge ([9cef51f](https://github.com/agrc/masquerade/commit/9cef51ff559300e701b430bee8fab8c6f49fefc7))

## [1.1.11-1](https://github.com/agrc/masquerade/compare/v1.1.11-0...v1.1.11-1) (2023-06-20)


### 📖 Documentation Improvements

* add time units ([8b95a26](https://github.com/agrc/masquerade/commit/8b95a2621b1cc1e3f4ef7300be85581398f7efa7))
* update code coverage badge ([f0017fa](https://github.com/agrc/masquerade/commit/f0017fa704617344d941fe46eaeb03a28deeef76))

## [1.1.11-0](https://github.com/agrc/masquerade/compare/v1.1.10...v1.1.11-0) (2023-06-19)


### 🐛 Bug Fixes

* handle missing keys in batch data ([65b9a42](https://github.com/agrc/masquerade/commit/65b9a426872a82d2d1c2edb1baf622c949da38c9))
* more retries on database queries with less wait ([1a74e1d](https://github.com/agrc/masquerade/commit/1a74e1d3cfc1f85649601c70aaab801685c6b306))

## [1.1.10](https://github.com/agrc/masquerade/compare/v1.1.9...v1.1.10) (2023-06-12)


### 🐛 Bug Fixes

* handle string values for max suggestions param ([#133](https://github.com/agrc/masquerade/issues/133)) ([9d6a739](https://github.com/agrc/masquerade/commit/9d6a739570a2fc8adcbf05650978efbe9cb2c1f3))

## [1.1.9](https://github.com/agrc/masquerade/compare/v1.1.8...v1.1.9) (2023-06-07)


### 🐛 Bug Fixes

* add defensive code to method ([ad36cf6](https://github.com/agrc/masquerade/commit/ad36cf6c52b2e07761ee23e668b30d5263452e17))

## [1.1.8](https://github.com/agrc/masquerade/compare/v1.1.7...v1.1.8) (2023-06-06)


### 🐛 Bug Fixes

* bump dependencies 🌲 ([a95c899](https://github.com/agrc/masquerade/commit/a95c899250f1d174f1318e0e3462389d4e0efa67))
* **ci:** add missing flag to cloud run deploy ([0961878](https://github.com/agrc/masquerade/commit/0961878783b6f3a4634fde1df060dbd7ca317244))
* cleanse inputs that may have issues ([44b0d08](https://github.com/agrc/masquerade/commit/44b0d08b4bdc4dba038965c839d4fe47dda9dddf)), closes [#124](https://github.com/agrc/masquerade/issues/124)
* **lint:** remove deprecated pylint option ([b5eaf8e](https://github.com/agrc/masquerade/commit/b5eaf8e21e225f6563f87dc3836d8594791b4b51))

## [1.1.8-2](https://github.com/agrc/masquerade/compare/v1.1.8-1...v1.1.8-2) (2023-06-05)


### 🐛 Bug Fixes

* cleanse inputs that may have issues ([1a95fdb](https://github.com/agrc/masquerade/commit/1a95fdb3b3d0fa31c1e6a2d50f97cb478b424192)), closes [#124](https://github.com/agrc/masquerade/issues/124)
* **lint:** remove deprecated pylint option ([0e6030f](https://github.com/agrc/masquerade/commit/0e6030f92d73f6f904d52107bc28d72397519525))

## [1.1.8-1](https://github.com/agrc/masquerade/compare/v1.1.8-0...v1.1.8-1) (2023-06-02)


### 🐛 Bug Fixes

* **ci:** add missing flag to cloud run deploy ([1613732](https://github.com/agrc/masquerade/commit/16137320eabde1ab4fc7298ed6a4316a7d7a8f9b))

## [1.1.8-0](https://github.com/agrc/masquerade/compare/v1.1.7...v1.1.8-0) (2023-06-02)


### 🐛 Bug Fixes

* bump dependencies 🌲 ([5d0dcbc](https://github.com/agrc/masquerade/commit/5d0dcbc43785dfeaab4f7de577b42382e923142c))

## [1.1.7](https://github.com/agrc/masquerade/compare/v1.1.6...v1.1.7) (2023-04-04)


### 🐛 Bug Fixes

* Q2 Dep Bumps 🌲 ([a4d027c](https://github.com/agrc/masquerade/commit/a4d027c2e8052012d51a5a062bd5ea364e71710a))

## [1.1.6](https://github.com/agrc/masquerade/compare/v1.1.5...v1.1.6) (2023-03-28)


### 🐛 Bug Fixes

* add timeout to requests to api.mapserv.utah.gov ([f977346](https://github.com/agrc/masquerade/commit/f9773461ebe2e522802c7ce41567891e869fbee8)), closes [#108](https://github.com/agrc/masquerade/issues/108)
* bump deps ([8b4e827](https://github.com/agrc/masquerade/commit/8b4e8275c44f0bc13f88c1cbeb32ab6f35acc9f6))

## [1.1.5](https://github.com/agrc/masquerade/compare/v1.1.4...v1.1.5) (2023-02-02)


### 🐛 Bug Fixes

* **tests:** don't throw generic exceptions ([80eb320](https://github.com/agrc/masquerade/commit/80eb3209690e578865274c08fd80b1a2406adf8d))

## [1.1.4](https://github.com/agrc/masquerade/compare/v1.1.3...v1.1.4) (2022-12-17)


### 🐛 Bug Fixes

* gracefully handle 404s from web api ([464e938](https://github.com/agrc/masquerade/commit/464e938a4878f1d43201349b9c6c4031f52e5adc)), closes [#98](https://github.com/agrc/masquerade/issues/98)

## [1.1.4-1](https://github.com/agrc/masquerade/compare/v1.1.3...v1.1.4-1) (2022-12-16)


### 🐛 Bug Fixes

* gracefully handle 404s from web api ([b6ded28](https://github.com/agrc/masquerade/commit/b6ded286f221a29ef369351db20343e534d99218)), closes [#98](https://github.com/agrc/masquerade/issues/98)

## [1.1.4-0](https://github.com/agrc/masquerade/compare/v1.1.2...v1.1.4-0) (2022-12-16)


### 🐛 Bug Fixes

* **deps:** update simplejson requirement from ==3.17.* to &gt;=3.17,&lt;3.19 ([85c93cc](https://github.com/agrc/masquerade/commit/85c93cc6557fe3a26aba0a4873e3577191f9efd1))
* gracefully handle 404s from web api ([9995ba5](https://github.com/agrc/masquerade/commit/9995ba5fd4cb0a34885e80ba3270a76eac653b8d)), closes [#98](https://github.com/agrc/masquerade/issues/98)

## [1.1.3](https://github.com/agrc/masquerade/compare/v1.1.2...v1.1.3) (2022-12-12)


### 🐛 Bug Fixes

* **deps:** update simplejson requirement from ==3.17.* to &gt;=3.17,&lt;3.19 ([ff1a8c6](https://github.com/agrc/masquerade/commit/ff1a8c6a3b4762c56f8610b956067e0173b8aca5))

## [1.1.3-0](https://github.com/agrc/masquerade/compare/v1.1.2...v1.1.3-0) (2022-12-09)


### 🐛 Bug Fixes

* **deps:** update simplejson requirement from ==3.17.* to &gt;=3.17,&lt;3.19 ([85c93cc](https://github.com/agrc/masquerade/commit/85c93cc6557fe3a26aba0a4873e3577191f9efd1))

## [1.1.2](https://github.com/agrc/masquerade/compare/v1.1.1...v1.1.2) (2022-11-21)


### 🐛 Bug Fixes

* **build:** add repo token input to prod deploy ([9aeebb1](https://github.com/agrc/masquerade/commit/9aeebb1c42ce36f8e1aa7a8a9896fb544925e0db))

## [1.1.1](https://github.com/agrc/masquerade/compare/v1.1.0...v1.1.1) (2022-11-18)


### 🐛 Bug Fixes

* add service now creds to deploy action ([416b0e9](https://github.com/agrc/masquerade/commit/416b0e9405371159ea6ef1305392236f1bdc771f))

## [1.1.0](https://github.com/agrc/masquerade/compare/v1.0.2...v1.1.0) (2022-11-14)


### 🚀 Features

* implement connection pooling ([53425b6](https://github.com/agrc/masquerade/commit/53425b64b93694ab8bd376c51d180284b9c6c174))


### 🐛 Bug Fixes

* handle invalid magicKey values ([4cb3995](https://github.com/agrc/masquerade/commit/4cb3995b3425cf373015669ee9226216b484547b))

## [1.0.2](https://github.com/agrc/masquerade/compare/v1.0.1...v1.0.2) (2022-10-06)


### 🐛 Bug Fixes

* bump pytest-cov ([a53811a](https://github.com/agrc/masquerade/commit/a53811a468bd7c3870983cf7a72d00a9d2cb75b6))

## [1.0.2-0](https://github.com/agrc/masquerade/compare/v1.0.1...v1.0.2-0) (2022-10-06)


### 🐛 Bug Fixes

* bump pytest-cov ([6aed19d](https://github.com/agrc/masquerade/commit/6aed19db72cc702066b908c0654cd33e3b620f34))

## [1.0.1](https://github.com/agrc/masquerade/compare/v1.0.0...v1.0.1) (2022-10-06)


### 🐛 Bug Fixes

* **ci:** checkout before calling local action ([603eff7](https://github.com/agrc/masquerade/commit/603eff728c554de432fe9b5add477ea5d86d31e2))
* **ci:** fix path to local action ([a3f1558](https://github.com/agrc/masquerade/commit/a3f1558a9c0b81fa2b80a670ad0519b6a8843e73))
* October dependency bumps 🌲 ([e96cd5c](https://github.com/agrc/masquerade/commit/e96cd5c8114070a5e128be062a3ffc93cb367456))

## [1.0.1-2](https://github.com/agrc/masquerade/compare/v1.0.1-1...v1.0.1-2) (2022-10-06)


### 🐛 Bug Fixes

* **ci:** fix path to local action ([cfda105](https://github.com/agrc/masquerade/commit/cfda10569084bfa3d2963e9fd022a5592fb15a47))

## [1.0.1-1](https://github.com/agrc/masquerade/compare/v1.0.1-0...v1.0.1-1) (2022-10-06)


### 🐛 Bug Fixes

* **ci:** checkout before calling local action ([53b3962](https://github.com/agrc/masquerade/commit/53b3962f43defc98037c06fd87e0cad65f006ed8))

## [1.0.1-0](https://github.com/agrc/masquerade/compare/v1.0.0...v1.0.1-0) (2022-10-06)


### 🐛 Bug Fixes

* October dependency bumps 🌲 ([3ea511a](https://github.com/agrc/masquerade/commit/3ea511a535b53e81712372408e1aecb0be7f7f0f))
