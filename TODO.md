# Make a tool to do this automatically base on this project:

https://github.com/stevenweaver/likely-neutral-with-steven-weaver/blob/master/tutorials/reviewbrah.md?plain=1

# Getting Every ReviewBrah Rating Using LLMs

## "Hello Everyone!"

A phrase that echoes throughout my house on weekly basis from my favorite YouTuber, ReviewBrah.

| Reviewed Item                                       | Restaurant         | Cost                             | Rating | Review Date |
| --------------------------------------------------- | ------------------ | -------------------------------- | ------ | ----------- |
| Caramel Apple Empanada                              | Taco Bell          | $2.99                            | 5.5    | 2024-12-09  |
| McDonald's McRib                                    | McDonald's         | $5.50                            | 9      | 2024-12-02  |
| Maple Bourbon Barbecue Whopper                      | Burger King        | $8.00                            | 7.4    | 2024-11-26  |
| Pickle Fries                                        | Burger King        | $5.00                            | 1.0    | 2024-11-26  |
| Big Clucking Chicken Sandwich                       | Applebee's         | $10.00                           | 9.4    | 2024-11-20  |
| Midnight Cherry Freeze                              | Taco Bell          | $3.80                            | 4.6    | 2024-11-16  |
| Shakaroni Pizza                                     | Papa John's        | $13.00                           | 9.2    | 2024-11-09  |
| Tostada                                             | Taco Bell          | $2.19                            | 6.0    | 2024-11-02  |
| Green Sauce Burrito                                 | Taco Bell          | $2.49                            | 4.9    | 2024-11-02  |
| Meximelt                                            | Taco Bell          | $3.00                            | 8.5    | 2024-11-02  |
| Gordita Supreme                                     | Taco Bell          | $2.99                            | 8.8    | 2024-11-02  |
| KFC Original Recipe Tenders                         | KFC                | $5.00                            | 7      | 2024-10-28  |
| KFC Comeback Sauce                                  | KFC                | -                                | 3      | 2024-10-28  |
| Wednesday's Whopper                                 | Burger King        | $7.00                            | 8      | 2024-10-20  |
| Things Rings                                        | Burger King        | $3.49                            | 6.8    | 2024-10-20  |
| Morticia Cookie Chocolate Shake                     | Burger King        | $5.00 - $6.00                    | 7.2    | 2024-10-20  |
| Chicken Big Mac                                     | McDonald's         | $6.00                            | 4.2    | 2024-10-15  |
| Krabby Patty collab Burger                          | Wendy's            | $9.00                            | 8.5    | 2024-10-08  |
| Pineapple under the sea Frosty                      | Wendy's            | $9.00                            | 8.6    | 2024-10-08  |
| Witches Brew Slush Float                            | Sonic              | $4.00                            | 9.2    | 2024-10-05  |
| Giant Cheez-It Tostada                              | Taco Bell          | $3.65                            | 8      | 2024-09-23  |
| Giant Cheez-It Crunch Wrap                          | Taco Bell          | $3.65                            | 8      | 2024-09-23  |
| Patty Melt                                          | Five Guys          | $10.00                           | 7      | 2024-09-18  |
| Bacon Burger                                        | Five Guys          | $10.00                           | 8      | 2024-09-18  |
| Cajun Fries                                         | Five Guys          | $5.00                            | 8      | 2024-09-18  |
| Sweet Barbecue Blaze Chicken Sandwich               | Wing Stop          | $6.79                            | 8.25   | 2024-09-12  |
| Mountain Dew Baja Blast Gelato                      | Taco Bell          | $4.00                            | 6.7    | 2024-09-05  |
| Honey Pepper Pimento Chicken Sandwich               | Chick-fil-A        | $7.55                            | 9.4    | 2024-08-30  |
| Bourbon Barbecue Chicken Sandwich                   | Arby’s             | $7.50 - $9.00                    | 0      | 2024-08-19  |
| Curly Fries                                         | Arby’s             | $2.00 - $3.00                    | 0      | 2024-08-19  |
| Jamoka Shake                                        | Arby’s             | $2.00 - $4.00                    | 5      | 2024-08-19  |
| KFC Saucy Nuggets                                   | KFC                | $17.25                           | 5.0    | 2024-08-13  |
| KFC Chipotle Ranch                                  | KFC                | $5.75                            | 3.0    | 2024-08-13  |
| KFC Mango Habanero                                  | KFC                | $5.75                            | 6.7    | 2024-08-13  |
| KFC Honey Garlic                                    | KFC                | $5.75                            | 5.0    | 2024-08-13  |
| Culver's JJ Watt Meal                               | Culver's           | $10.00                           | 8.5    | 2024-08-09  |
| Cheese Curds                                        | Culver's           | $10.00                           | 8.5    | 2024-08-09  |
| Culver's Deluxe Burger                              | Culver's           | $10.00                           | 8.5    | 2024-08-09  |
| Root Beer                                           | Culver's           | $10.00                           | 8.5    | 2024-08-09  |
| Sonic Smasher                                       | Sonic              | $10.00                           | 8      | 2024-08-03  |
| Fiery Strawberry Sprite                             | Burger King        | $3.23                            | 8      | 2024-07-29  |
| Fiery Mozzarella Fries                              | Burger King        | $5.15                            | 7      | 2024-07-29  |
| Fiery Bacon Whopper                                 | Burger King        | $8.40                            | 8.4    | 2024-07-29  |
| Fiery Chicken Fries                                 | Burger King        | $4.79                            | 4      | 2024-07-29  |
| Fiery Bacon Royal Krispy Chicken Sandwich           | Burger King        | $8.40                            | 2      | 2024-07-29  |
| Cheesy Street Chalupa                               | Taco Bell          | $5.50                            | 4      | 2024-07-23  |
| Taco Bell $7 Lux Cravings Box                       | Taco Bell          | $9.00                            | 8.6    | 2024-07-17  |
| Smoky BLT Quarter Pounder                           | McDonald's         | $8.00                            | 5.5    | 2024-07-12  |
| KitKat Banana Split McFlurry                        | McDonald's         | $5.00                            | 8.2    | 2024-07-12  |
| Boneless Wings (Classic)                            | Popeyes            | $8.00                            | 6.0    | 2024-07-04  |
| Boneless Wings (Signature Hot)                      | Popeyes            | $8.00                            | 4.0    | 2024-07-04  |
| Boneless Wings (Honey Barbecue)                     | Popeyes            | $8.00                            | 8.1    | 2024-07-04  |
| $5 Meal Deal                                        | McDonald's         | $5.00                            | 8.8    | 2024-06-28  |
| Big Cheesy Bacon Burger                             | Arby's             | $10.00                           | 8.5    | 2024-06-24  |
| Chicago Tavern Style Pizza                          | Pizza Hut          | $12.00                           | 8      | 2024-06-19  |
| Maple pepper bacon chicken sandwich                 | Chick-fil-A        | $11.00                           | 9      | 2024-06-14  |
| Saucy Nuggets - Honey Barbecue                      | Wendy's            | $4.00                            | 8.3    | 2024-06-10  |
| Saucy Nuggets - Spicy Ghost Pepper                  | Wendy's            | $4.00                            | 3.0    | 2024-06-10  |
| Big Chee-it Crunch Wrap Supreme                     | Taco Bell          | $6.00                            | 6.7    | 2024-06-05  |
| Mr Beast Box                                        | Zach Bees          | $15.00                           | 7.8    | 2024-05-31  |
| Pizza Hut Cheeseburger Melt                         | Pizza Hut          | $8.00                            | 2      | 2024-05-27  |
| Grandma McFlurry                                    | McDonald's         | $5.00                            | 9      | 2024-05-22  |
| Philly Melt                                         | Burger King        | $6.50                            | 4      | 2024-05-21  |
| Barbecue Bacon Chicken Sandwich                     | Denny's            | $20.00                           | 3      | 2024-05-16  |
| Golden Barbecue Chicken Sandwich                    | Popeyes            | $8.00                            | 7      | 2024-05-10  |
| Chicken Tenders Meal                                | Popeyes            | $20.00                           |        | 2024-05-10  |
| Barbecue Chicken Wrap                               | Arby's             | $3.00                            | 8      | 2024-05-06  |
| Bacon Cajun Ranch MC Krispy Sandwich                | McDonald's         | $6.00                            | 4      | 2024-05-01  |
| Nacho Fries                                         | Taco Bell          | $6.00                            | 7      | 2024-04-27  |
| Bacon Cajun Ranch Deluxe MC Krispy Chicken Sandwich | McDonald's         | $7.30                            | 8.5    | 2024-04-22  |
| New York Style Pizza                                | Domino's           | $18.00                           | 6      | 2024-04-17  |
| Cantina crispy chicken taco                         | Taco Bell          | $3.65                            | 9.1    | 2024-04-12  |
| Spicy Chicken McNuggets                             | McDonald's         | $5.30                            | 8.0    | 2024-04-06  |
| KFC Saucy Nuggets (Korean Barbecue)                 | KFC                | $5.99                            | 4.8    | 2024-04-02  |
| KFC Saucy Nuggets (Honey Sriracha)                  | KFC                | $5.99                            | 4.8    | 2024-04-02  |
| KFC Saucy Nuggets (Sticky Chicky)                   | KFC                | $5.99                            | 4.8    | 2024-04-02  |
| KFC Saucy Nuggets (Nashville Hot)                   | KFC                | $5.99                            | 4.8    | 2024-04-02  |
| KFC Saucy Nuggets (Georgia Gold)                    | KFC                | $5.99                            | 4.8    | 2024-04-02  |
| Crispy Cupy Roni Pizza                              | Papa John's        | $14.00                           | 8      | 2024-03-27  |
| Honey Lemon Pepper Wings                            | Popeyes            | $8.00                            | 2      | 2024-03-20  |
| Crazy Puffs                                         | Little Caesars     | $4.81                            | 7.4    | 2024-03-15  |
| Fiery Chicken Nuggets                               | Burger King        | $2.99                            | 6      | 2024-03-10  |
| Fiery Buffalo Royal Crispy Wrap                     | Burger King        | $3.00                            | 3.5    | 2024-03-10  |
| wicd Donald's sauce                                 | McDonald's         | $0.50                            | 7      | 2024-03-05  |
| Cheesa                                              | KFC                | $12.00                           | 8      | 2024-02-26  |
| Chicken Sandwich                                    | Wendy's            | $8.00                            | 7      | 2024-02-26  |
| Big Mac                                             | McDonald's         | $5.00                            | 9      | 2024-02-26  |
| Pizza                                               | Domino's           | $15.00                           | 6      | 2024-02-26  |
| Burrito                                             | Chipotle           | $10.00                           | 8      | 2024-02-26  |
| Wing Stop Hot Honey Chicken Sandwich                | Wing Stop          | $6.79                            | 5.9    | 2024-02-21  |
| Cheesy Chicken Crispata                             | Taco Bell          | $3.50                            | 6      | 2024-02-16  |
| Candied Bacon Whopper                               | Burger King        | $8.40                            | 8.9    | 2024-02-09  |
| Hot Honey Pizza                                     | Pizza Hut          | $16.00                           | 7.2    | 2024-02-04  |
| Double Big Mac                                      | McDonald's         | $7.50                            | 7      | 2024-01-30  |
| Breakfast Burrito                                   | Wendy's            | $4.00                            | 6      | 2024-01-26  |
| Shake Shack Korean Style Fried Chicken Sandwich     | Shake Shack        | $11.00                           | 6      | 2024-01-23  |
| Peanut Butter Bacon Cheeseburger                    | Sonic Drive-In     | $6.00                            | 5.8    | 2024-01-18  |
| Three Cheese Chicken Flatbread Melt                 | Taco Bell          | $2.30                            | 7      | 2024-01-13  |
| Slices and Sticks Pizza                             | Little Caesars     | $8.00                            | 9      | 2024-01-09  |
| KFC Honey Barbecue Wrap                             | KFC                | $3.00                            | 6.1    | 2024-01-04  |
| KFC Spicy Mac & Cheese Wrap                         | KFC                | $3.00                            | 4.9    | 2024-01-04  |
| KFC Chicken Nuggets                                 | KFC                | $5.00                            | 8.8    | 2023-12-31  |
| Taco Bell Crispy Chicken Wings                      | Taco Bell          | Not specified                    | 8.9    | 2023-12-31  |
| Taco Bell Grilled Cheese Burrito                    | Taco Bell          | $4.79                            | 9.0    | 2023-12-31  |
| Pineapple Pepsi                                     | Little Caesars     | Not specified                    | 9.0    | 2023-12-31  |
| Chick-fil-A Honey Pepper Pimento Chicken Sandwich   | Chick-fil-A        | $9.00                            | 9.3    | 2023-12-31  |
| Loaded Tots                                         | Domino's           | $7.00                            | 3.5    | 2023-12-31  |
| Salsa Verde Grilled Chicken Burrito                 | Taco Bell          | $2.00                            | 3      | 2023-12-31  |
| Spicy Melt                                          | Burger King        | $6.00                            | 3      | 2023-12-31  |
| Bourbon Barbecue Country Style Rib Sandwich         | Arby's             | $8.00                            | 2      | 2023-12-31  |
| Italian Original Chicken Sandwich                   | Burger King        | $6.00                            | 2      | 2023-12-31  |
| Papa John's Cheesy Calzone Stuffed Crust Pizza      | Papa John's        | $15.00                           | 8.35   | 2023-12-22  |
| Bacon Melt                                          | Burger King        | $6.50                            | 7.5    | 2023-12-17  |
| Cheesy Tots                                         | Burger King        | $1.50                            | 7.2    | 2023-12-17  |
| Empty Food                                          | McDonald's         | $14.00                           | 8.5    | 2023-12-11  |
| Double Decker Taco                                  | Taco Bell          | $3.70                            | 5.8    | 2023-12-08  |
| Signature Hot Wings                                 | Popeyes            | $8.00                            | 6      | 2023-12-04  |
| Honey Barbecue Wings                                | Popeyes            | $8.00                            | 8      | 2023-12-04  |
| Roasted Garlic Parmesan Wings                       | Popeyes            | $8.00                            | 5      | 2023-12-04  |
| Pretzel Baconator                                   | Wendy's            | $8.70                            | 8.3    | 2023-11-30  |
| Crazy Crust Pizza                                   | Little Caesars     | $11.50                           | 4      | 2023-11-25  |
| MC Rib                                              | McDonald's         | $6.50                            | 7.0    | 2023-11-19  |
| Good Burger 2 Meal                                  | Arby's             | $13.50                           | 7.2    | 2023-11-14  |
| Breakfast Taco Sausage                              | Taco Bell          | $2.00                            | 7.9    | 2023-11-09  |
| Burger with bacon                                   | Culver's           | N/A                              | 1/5    | 2023-11-04  |
| Fried Mac and Cheese Bites                          | Arby's             | $4.50 - $5.00                    | 4      | 2023-11-02  |
| Roasted Garlic Cheese Sticks                        | Pizza Hut          | $14.00                           | 7.7    | 2023-10-27  |
| Spicy Truff Chicken Sandwich                        | Popeyes            | $8.00                            | 4      | 2023-10-24  |
| KFC Jamal Murray Meal                               | KFC                | $11.00                           | 6.4    | 2023-10-21  |
| Steak and Bacon Grilled Cheese Burrito              | Taco Bell          | $7.00                            | 8.2    | 2023-10-16  |
| Ghost Pepper Whopper                                | Burger King        | $8.40                            | 8.1    | 2023-10-13  |
| Ghost Pepper Chicken Fries                          | Burger King        | $5.00                            | 3.0    | 2023-10-13  |
| Cheeseburger                                        | Joe's Diner        | $12.99                           | 4.5    | 2023-09-26  |
| Pepperoni Pizza                                     | Pizza Palace       | $15.00                           | 4.0    | 2023-09-25  |
| Caesar Salad                                        | Healthy Greens     | $10.50                           | 5.0    | 2023-09-24  |
| Chicken Tikka                                       | Curry House        | $14.99                           | 4.8    | 2023-09-23  |
| Sushi Platter                                       | Tokyo Sushi        | $25.00                           | 4.9    | 2023-09-22  |
| Spaghetti Bolognese                                 | Italian Bistro     | $18.00                           | 4.4    | 2023-09-21  |
| Tacos                                               | Taco Time          | $10.00                           | 4.2    | 2023-09-20  |
| Steak Frites                                        | Grill House        | $22.50                           | 4.7    | 2023-09-19  |
| Chocolate Cake                                      | Sweet Tooth Bakery | $5.50                            | 4.6    | 2023-09-18  |
| Pad Thai                                            | Bangkok Cuisine    | $13.50                           | 4.3    | 2023-09-17  |
| Pepperoni Stuffed Cheesy Bread                      | Domino's           | $7.00                            | 7      | 2023-10-06  |
| Honey Mustard BK Royal Crispy Chicken Sandwich      | Burger King        | $8.00                            | 2      | 2023-09-30  |
| Chicken Enchilada Burrito                           | Taco Bell          | $2.00                            | 3      | 2023-09-24  |
| Big Game Burger                                     | Arby's             | $9.00                            | 7.1    | 2023-09-18  |
| Hot and Spicy Wings                                 | KFC                | $6.00                            | 7.4    | 2023-09-14  |
| Four Quarter Calzone                                | Little Caesars     | $9.00                            | 7      | 2023-09-09  |
| Sweet and Spicy Wings                               | Popeyes            | $6.00                            | 8.8    | 2023-09-06  |
| Honey Pepper Pimento Chicken Sandwich               | Chick-fil-A        | $9.00                            | 9.3    | 2023-09-01  |
| Caramel Crumble Milkshake                           | Chick-fil-A        | $2.00                            | 6.7    | 2023-09-01  |
| Loaded Nacho Cheeseburger                           | Wendy's            | $8.00                            | 6.7    | 2023-08-26  |
| BK Royal Crispy Chicken Wrap                        | Burger King        | $3.00                            | 5.8    | 2023-08-21  |
| Big Mac Meal                                        | McDonald's         | $14.00                           | 6      | 2023-08-14  |
| Italian Original Chicken Sandwich                   | Burger King        | $6.00                            | 2      | 2023-08-12  |
| Grilled Cheese Dipping Taco                         | Taco Bell          | $3.50                            | 6.7    | 2023-08-07  |
| Deluxe Box                                          | Taco Bell          | $10.00                           | 6.7    | 2023-08-07  |
| Blazin Knockout Wings                               | Buffalo Wild Wings | $11.00                           | 8.5    | 2023-08-01  |
| Garlic Epic Stuffed Crust Pizza                     | Papa John's        | $14.00                           | 8      | 2023-07-25  |
| Pepsi Pineapple                                     | Little Caesars     | $2.00                            | 9      | 2023-07-21  |
| Cheesy Jalapeno Bacon Quarter Pounder               | McDonald's         | $8.00                            | 8.4    | 2023-07-15  |
| Crispy Chicken Taco                                 | Taco Bell          | $3.00                            | 4      | 2023-07-11  |
| Ultimate Barbecue Chicken Sandwich                  | KFC                | $7.00                            | 7.3    | 2023-07-05  |
| Volcano Taco                                        | Taco Bell          | $2.49                            | 8      | 2023-06-28  |
| Volcano Burrito                                     | Taco Bell          | $4.00                            | 7.2    | 2023-06-28  |
| Fiery Chicken Nuggets                               | Burger King        | $2.99                            | 8.5    | 2023-06-24  |
| Boneless Wings                                      | Papa John's        | $8.50 (10 pcs)                   | 5.5    | 2023-06-19  |
| Boneless Wings                                      | Papa John's        | $11.00 (15 pcs)                  | -      | 2023-06-19  |
| Boneless Wings                                      | Papa John's        | $21.00 (30 pcs)                  | -      | 2023-06-19  |
| Grimace Birthday Meal                               | McDonald's         | $13.50                           | 8      | 2023-06-12  |
| Popeyes Bacon and Cheese Chicken Sandwich           | Popeyes            | $7.00                            | 4      | 2023-06-09  |
| Sweet Chili Lime Wings                              | Buffalo Wild Wings | $25.00                           | 5      | 2023-06-05  |
| General Tso's Chicken Wings                         | Buffalo Wild Wings | $25.00                           | 8.4    | 2023-06-05  |
| Steak Chile Verde Fries Burrito                     | Taco Bell          | $5.00                            | 6      | 2023-05-31  |
| Bacon Ranch Wagyu Steakhouse Burger                 | Arby's             | $8.00                            | 6.7    | 2023-05-26  |
| Spider-Verse Whopper                                | Burger King        | $6.50                            | 8.6    | 2023-05-21  |
| Spider-Verse Sundae                                 | Burger King        | $3.00                            | 8.6    | 2023-05-21  |
| Bourbon Barbecue Country Style Rib Sandwich         | Arby's             | $8.00                            | 2      | 2023-05-16  |
| Ghost Pepper Ranch Chicken Sandwich                 | Wendy's            | $8.00                            | 6      | 2023-05-12  |
| Doritos Cool Ranch Chicken Papadia                  | Papa John's        | $7.99                            | 7.5    | 2023-05-08  |
| Cheese Steak Melt                                   | Pizza Hut          | $8.53                            | 3.5    | 2023-05-03  |
| Grilled Cheese Burrito                              | Taco Bell          | $4.79                            | 9      | 2023-04-26  |
| Spicy Chicken Nuggets                               | McDonald's         | $7.00                            | 8.6    | 2023-04-22  |
| Nacho Fries 2023 Edition                            | Taco Bell          | $3.50                            | 8.9    | 2023-04-17  |
| Whopper Melt                                        | Burger King        | $7.00                            | 3      | 2023-04-10  |
| Spicy Melt                                          | Burger King        | $6.00                            | 3      | 2023-04-10  |
| Regular Burger                                      | Burger King        | $5.00                            | 7      | 2023-04-10  |
| Chicken Sandwich                                    | Burger King        | $5.00                            | 6      | 2023-04-10  |
| Whopper                                             | Burger King        | $8.00                            | 8      | 2023-04-10  |
| KFC Chicken Nuggets                                 | KFC                | $5.00                            | 8.8    | 2023-04-05  |
| Little Caesars Pretzel Crust Pizza                  | Little Caesars     | $7.00                            | 8      | 2023-03-29  |
| Honey Barbecue Wings                                | Buffalo Wild Wings | $12.00                           | 4.5    | 2023-03-27  |
| Medium Wings                                        | Buffalo Wild Wings | $12.00                           | 3.0    | 2023-03-27  |
| Bacon Club Chalupa                                  | Taco Bell          | $5.00                            | 8.15   | 2023-03-22  |
| McDonald's Bacon Ranch McCrispy Sandwich            | McDonald's         | $7.50                            | 4      | 2023-03-17  |
| Spicy Chicken Fries                                 | Burger King        | $8.00                            | 8      | 2023-03-13  |
| Double Down Sandwich                                | KFC                | $11.50                           | 7.6    | 2023-03-07  |
| Kentucky Fried Wrap                                 | KFC                | $3.50                            | 7.5    | 2023-03-01  |
| Cheddar Bacon Loaded Tots                           | Domino's           | $7.00                            | 3.5    | 2023-02-23  |
| Cheeseburger with Barbecue Sauce                    | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| Quarter Pounder with Cheese                         | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| Large Fries                                         | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| Apple Pie                                           | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| Large Coke                                          | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| High C Orange                                       | McDonald's         | $18.00                           | 6.5    | 2023-02-16  |
| Big New Yorker Pizza                                | Pizza Hut          | $13.99                           | 8.7    | 2023-02-11  |
| Crispy Melt Taco                                    | Taco Bell          | $2.49                            | 5.8    | 2023-02-06  |
| Papa John’s Crispy Parm Pizza                       | Papa John's        | $12.99                           | 7      | 2023-01-31  |
| Crispy Chicken Wings                                | Taco Bell          | $9.00                            | 8.9    | 2023-01-24  |
| Mexican Original Chicken Sandwich                   | Burger King        | $6.00                            | 5.5    | 2023-01-13  |
| Ghost Pepper Wings                                  | Popeyes            | $12.00                           | 6.5    | 2023-01-07  |
| Salsa Verde Grilled Chicken Burrito                 | Taco Bell          | $2.00                            | 7.5    | 2023-01-02  |
| Salsa Verde Grilled Chicken Burrito                 | Taco Bell          | $2.00                            | 3      | 2023-01-02  |
| Oreo cookie Papa bites                              | Papa John's        | $5.00                            | 4.8    | 2022-12-27  |
| Seven Layer Nacho Fries Bowl                        | Taco Bell          | $3.49                            | 6      | 2022-12-20  |
| Breakfast Crunchwrap                                | Taco Bell          | $4.00                            | 6.5    | 2022-12-20  |
| Italian Sandwich                                    | Wendy's            | $X.XX                            | 1      | 2022-12-12  |
| Carolina Gold BBQ Sandwich                          | Wingstop           | $6.40                            | 7      | 2022-12-12  |
| Italian Mozzarella Chicken Sandwich                 | Wendy's            | $8.50                            | 1.5    | 2022-12-02  |
| Smoky BLT Quarter Pounder with Cheese               | McDonald's         | $8.00                            | 9      | 2022-11-26  |
| Blackened Chicken Sandwich                          | Popeyes            | $6.00                            | 3      | 2022-11-19  |
| Pizza Hut Melt                                      | Pizza Hut          | $8.40                            | 9      | 2022-11-12  |
| McRib                                               | McDonald's         | $5.70                            | 5.6    | 2022-11-05  |
| Arby's Diablo Sandwich                              | Arby's             | $6.79                            | 8.5    | 2022-10-28  |
| Ghost Pepper Whopper                                | Burger King        | $9.00                            | 8.4    | 2022-10-18  |
| Wing Stop Chicken Sandwich                          | Wing Stop          | $7.00                            | 5.5    | 2022-10-12  |
| Cactus Plant Flea Market Meal                       | McDonald's         | $11.50                           | 7      | 2022-10-04  |
| Hot Ones Burger                                     | Shake Shack        | $10.00                           | 8      | 2022-09-28  |
| Detroit Style Pizza                                 | Pizza Hut          | $14.00                           | 7      | 2022-09-15  |
| Royal Crispy Chicken Sandwich                       | Burger King        | $5.50                            | 4.9    | 2022-09-14  |
| Hot Honey Not Bird Person Combo                     | Wendy's            | $11.50                           | 6      | 2022-09-08  |
| Italian Meat Trio Bowl                              | Papa John's        | $8.00                            | 3      | 2022-08-29  |
| Grilled Cheese Burrito                              | Taco Bell          | $7.00                            | 7.0    | 2022-08-22  |
| Grilled Cheese Burrito                              | Taco Bell          | $6.00                            | 7.75   | 2021-11-01  |
| Home Style French Toast Sticks                      | Wendy's            | $2.79                            | 2      | 2022-08-17  |
| Crispy Chicken Sandwich Meal Deal                   | McDonald's         | $8.00                            | 5      | 2022-08-11  |
| Old World Fanceroni Pizza                           | Little Caesars     | $10.00                           | 7.2    | 2022-08-05  |
| Hush Puppy Breaded Fish Strips                      | Arby's             | $4.30 (3 piece), $6.29 (6 piece) | 6.0    | 2022-08-01  |
| Buffalo Wild Wings Saucy Chicken Sandwich           | Buffalo Wild Wings | $10.50                           | 5.9    | 2022-07-26  |
| Chicken Sandwich Meal                               | Popeyes            | $6.00                            | 7.8    | 2022-07-21  |
| Cantina Crispy Chicken Taco                         | Taco Bell          | $3.00                            | 1      | 2022-07-15  |
| Southwest Bacon Whopper                             | Burger King        | $7.00                            | 6      | 2022-07-11  |
| Impossible King                                     | Burger King        | $7.00                            | 8.5    | 2022-07-05  |
| Whopper                                             | Burger King        | $7.00                            | N/A    | 2022-07-05  |
| Classic Cheesy Double Beef Burrito                  | Taco Bell          | $2.00 - $2.50                    | 7.5    | 2022-06-30  |
| Honey Barbecue Bird Dog                             | Buffalo Wild Wings | $10.00                           | 5      | 2022-06-25  |
| Wisconsin Big Cheese Pub Burger                     | Culver's           | $7.00                            | 3      | 2022-06-20  |
| Toasted Cheddar Chalupa                             | Taco Bell          | $4.19                            | 8.5    | 2022-06-16  |
| Edge Pizza                                          | Pizza Hut          | $13.00                           | 9      | 2022-06-10  |
| Thin & Crispy Crust                                 | Pizza Hut          | $13.00                           | 9      | 2022-06-10  |
| Jack Harlow Meal                                    | KFC                | $10.79                           | 8      | 2022-06-06  |
| Spicy Chicken Sandwich                              | KFC                | Included                         | 8      | 2022-06-06  |
| Mac and Cheese                                      | KFC                | Included                         | 6      | 2022-06-06  |
| Secret Recipe Fries                                 | KFC                | Included                         | 8      | 2022-06-06  |
| Lemonade                                            | KFC                | Included                         | 7      | 2022-06-06  |
| Deluxe Wagyu Steakhouse Burger                      | Arby's             | $6.49                            | 8      | 2022-05-30  |
| Mexican Pizza                                       | Taco Bell          | $5.00                            | 3      | 2022-05-23  |
| Spicy Take Chicken Sandwich                         | Panera Bread       | $13.00                           | 6.8    | 2022-05-19  |
| Bourbon Bacon Cheddar Burger                        | Shake Shack        | $10.00                           | 3      | 2022-05-12  |
| Popeye's Buffalo Ranch Chicken Sandwich             | Popeyes            | $5.00                            | 7.6    | 2022-05-06  |
| Epic Stuffed Crust Pizza                            | Papa John's        | $20.00                           | 9      | 2022-05-01  |
| Detroit Style Deep Dish Pizza                       | Little Caesars     | $12.00                           | 8      | 2022-04-25  |
| Steak White Hot Ranch Fries Burrito                 | Taco Bell          | $3.49                            | 9      | 2022-04-18  |
| Popeyes Surf and Turf Combo                         | Popeyes            | $8.00                            | 8.2    | 2022-04-11  |
| Spicy Chicken Nuggets                               | McDonald's         | $7.00                            | 8      | 2022-04-05  |
| McDonald's Szechuan Sauce                           | McDonald's         | $2.00                            | 8.5    | 2022-03-31  |
| Dippable Chicken Nuggets                            | McDonald's         | $3.00                            | 8.5    | 2022-03-31  |
| French Fries                                        | McDonald's         | $2.00                            | 8.5    | 2022-03-31  |
| Szechuan Sauce                                      | McDonald's         | Complimentary                    | 8.5    | 2022-03-31  |
| Spicy Chicken Sandwich                              | KFC                | $5.60                            | 7      | 2022-03-27  |
| Secret Recipe Fries                                 | KFC                | $3.00                            | 7      | 2022-03-27  |
| Famous Biscuits                                     | KFC                | $2.00                            | 7      | 2022-03-27  |
| Steak Nacho Fries Burrito                           | Taco Bell          | $5.00                            | 7      | 2022-03-21  |
| Cherry Sunrise Freeze                               | Taco Bell          | $3.30                            | 8      | 2022-03-21  |
| Spicy Flounder Fish Sandwich                        | Popeyes            | $5.49                            | 2      | 2022-03-09  |
| Big King                                            | Burger King        | $6.00                            | 5      | 2022-03-03  |
| Coca-Cola Starlight                                 | Coca-Cola          | $2 - $5                          | 8.7    | 2022-02-28  |
| Coca-Cola Starlight Zero Sugar                      | Coca-Cola          | $2 - $5                          | 4      | 2022-02-28  |
| Hash Brown McMuffin                                 | McDonald's         | $9.00                            | 7      | 2022-02-20  |
| Taco Bell Cantina Crispy Chicken Taco               | Taco Bell          | $4.00                            | 6.5    | 2022-02-15  |
| Hot Honey Chicken Sandwich                          | Wendy's            | $10.00                           | 8.6    | 2022-02-10  |
| Spicy Lovers Pizza                                  | Pizza Hut          | $13.00                           | 8.5    | 2022-02-05  |
| Land Air and Sea                                    | McDonald's         | $8.00                            | 3      | 2022-01-31  |
| Batman Calzone                                      | Little Caesars     | $8.00                            | 5.8    | 2022-01-26  |
| Diablo Dare Sandwich                                | Arby's             | $6.00                            | 7.4    | 2022-01-18  |
| Beyond Fried Chicken                                | KFC                | $7.00                            | 0.5    | 2022-01-12  |
| Little Caesars Pizza                                | Little Caesars     | $5.55                            | 6.7    | 2022-01-05  |
| Marketing and Deception                             | Little Caesars     | $5.55                            | 2.0    | 2022-01-05  |
| New York Style Pizza                                | Papa John's        | $13.00                           | 7.7    | 2021-12-27  |
| Spicy Tender Sandwich                               | PDQ                | $7.25                            | 5.7    | 2021-12-22  |
| Small Fries                                         | Wendy's            | $1.69                            | 7.7    | 2021-12-10  |
| Medium Fries                                        | McDonald's         | $3.19                            | 7.9    | 2021-12-10  |
| Small Fries                                         | Burger King        | $2.39                            | 4.0    | 2021-12-10  |
| Cheetos Boneless Wings                              | Applebee's         | $11.99                           | 6.5    | 2021-11-27  |
| Italian Original Chicken Sandwich                   | Burger King        | $7.00                            | 2      | 2021-11-23  |
| McRib                                               | McDonald's         | $3.00 - $5.00                    | 5      | 2021-11-05  |
| Triple Bacon Pizza                                  | Papa John's        | $13.00                           | 8.2    | 2021-10-27  |
| Ghost Pepper Chicken Nuggets                        | Burger King        | $1.49 (8 pcs)                    | 5.4    | 2021-10-13  |
| Cantina Crispy Melt Taco                            | Taco Bell          | $2.19                            | 7.7    | 2021-10-08  |
| Detroit Style Pizza                                 | Pizza Hut          | $13.00                           | 9      | 2021-09-15  |
| Big Bacon Cheddar Cheeseburger                      | Wendy's            | $7.00                            | 7.8    | 2021-09-09  |
| Crispy Chicken Sandwich Taco                        | Taco Bell          | $2.49                            | 5.5    | 2021-09-04  |
| Chakaroni Pizza                                     | Papa John's        | $13.00                           | 8      | 2021-09-01  |
| Loaded Taco Fries Burrito                           | Taco Bell          | $3.00                            | 6      | 2021-08-26  |
| Crazy Calzone Pepperoni                             | Little Caesars     | $8.50                            | 7.4    | 2021-08-19  |
| Big Dinner Box                                      | Pizza Hut          | $23.00                           | 8.3    | 2021-08-14  |

## How I did it

The process includes retrieving transcripts, aligning them with upload dates,
crafting a custom LLM prompt, and performing a final cleanup pass.

### Step 1: Installing and Using youtube-transcript

Install the youtube-transcript tool:

```
cargo install youtube-transcript
```

I then tested the installation by downloading a single transcript:

```
youtube-transcript "https://www.youtube.com/watch?v=V4PO9nsW3aU" > reviewbrah2.txt
```

At this point, reviewbrah2.txt contains raw transcript text of the single video.

### Step 2: Listing All Videos in a Channel

I used yt-dlp to retrieve a list of videos from the channel

```
yt-dlp -s --flat-playlist --print-to-file url list.txt "https://www.youtube.com/@TheReportOfTheWeek/videos"
```

Your list.txt might look like:

```
https://www.youtube.com/watch?v=w_fCkwqW0DM
https://www.youtube.com/watch?v=Rys_CRK76sg
https://www.youtube.com/watch?v=V4PO9nsW3aU
...
```

Each line includes only the corresponding video URL.

### Step 3: Downloading Transcripts for Each Video

Use a loop to process every URL in list.txt and download the corresponding transcripts:

```
while read -r date url; do
video_id=$(echo "$url" | awk -F'v=' '{print $2}')
    youtube-transcript "$url" > "${video_id}\_output.txt"
done < list.txt
```

Now you have `\*\_output.txt` transcript for each video.

### Step 4: Prepending the Upload Date to Each Transcript

Next, prepend the corresponding upload date to the top of each transcript file:

I noticed that the transcripts didn't have a date in the files, so I had to go
back to retrieve them, then annotate each transcript.

First, get the dates for each transcript:

```
yt-dlp --skip-download \\n  --print-to-file "%(upload_date)s %(webpage_url)s" list.txt \\n  "https://www.youtube.com/@TheReportOfTheWeek/videos"
```

Then prepend each transcript with the correct date

```
while read -r date url; do
video_id=$(echo "$url" | awk -F'v=' '{print $2}')
    {
        echo "$date"
cat "${video_id}_output.txt"
    } > temp && mv temp "${video_id}\_output.txt"
done < list.txt
```

Now each transcript starts with its upload date

### Step 5: Crafting a Custom LLM Prompt

The LLM prompt must be precise so the model outputs only a markdown table. You may need to experiment to remove headers or other extraneous text. For example:

```
llm --system "Output only a markdown table with rows of data for columns: Reviewed Item, Restaurant, Cost, Rating, Review Date. Do not include a header row or any text other than the table rows themselves." --save reviewbrah
```

I had to adjust this prompt a bit to get the desired output format, and even then there would be some inconsistencies from time to time.

### Step 6: Feeding Transcripts into the LLM

Combine the transcript files with list.txt and feed them into the LLM using the refined prompt:

```
while read -r date url; do
video_id=$(echo "$url" | awk -F'v=' '{print $2}')
    files-to-prompt "${video_id}\_output.txt" | llm -t reviewbrah
done < list.txt | tee -a combined_output.txt
```

At this stage, you have a combined table spanning multiple videos, but it may still need cleanup due to inconsistencies in llm output, but just use llm again to clean up its mess.

### Step 7: Cleaning and Normalizing the Final Table

Perform a final cleanup step to ensure dates follow YYYY-MM-DD format and that no extraneous text remains:

```
cat combined_output.txt | llm --system "Clean this output up and make a singular markdown file from it, ensure all dates follow YYYY-MM-DD format. Only output the markdown table." > table.md
```

table.md now contains a unified markdown table. All dates are normalized, and the table is ready to publish.

### Conclusion

By combining:
• youtube-transcript to extract text
• yt-dlp to get metadata and dates at a channel level
• Shell scripting to align transcripts with their upload dates
• A carefully crafted LLM prompt to ensure the correct table format
• A final cleanup pass with the LLM

…you produce a neat, organized markdown table.
