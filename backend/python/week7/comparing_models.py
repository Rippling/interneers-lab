import time
from week7.semantic_search import semantic_search

GENERAL_TEST_QUERIES = [
    "construction toys",
    "gifts for toddlers",
    "pretend play toys",
    "science and learning toys",
    "soft cuddly toys",
]

MANUAL_RATING_QUERY = "toys for 5-year-olds"


def print_result_for_model(model_name, query, top_k=5):
    start_time = time.time()

    results = semantic_search(
        query=query,
        top_k=top_k,
        model_name=model_name,
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\n" + "=" * 50)
    print(f"MODEL: {model_name}")
    print(f"QUERY: {query}")
    print(f"TIME : {elapsed_time:.4f} seconds")
    print("=" * 50)

    if not results:
        print("No results found")
        return results, elapsed_time

    print("Top Results:")
    print("-" * 50)

    for rank, item in enumerate(results, start=1):
        print(f"{rank}. {item['name']}")
        print(f"   Score      : {item['semantic_score']:.4f}")
        print(f"   Description: {item['description']}")
        print(f"   Category   : {item['category']}")
        print(f"   Brand      : {item['brand']}")
        print(f"   Price      : {item['price']}")
        print(f"   Quantity   : {item['quantity']}")
        print()

    return results, elapsed_time


def general_comparision():
    model_name = [
        "all-MiniLM-L6-v2",
        "all-mpnet-base-v2",
    ]
    top_k = 5
    for model_name in model_name:
        print("\n" + "#"*50)
        print(f"MODEL: {model_name}")
        print("#"*50)
        total_time = 0.0
        for query in GENERAL_TEST_QUERIES:
            results, elapsed_time = print_result_for_model(
                model_name=model_name,
                query=query,
                top_k=top_k
            )
            total_time += elapsed_time
        print(f"Total Time for {model_name}: {total_time:.4f} seconds")


def manual_comparision():
    model_name = [
        "all-MiniLM-L6-v2",
        "all-mpnet-base-v2",
    ]
    top_k = 5
    print("\n" + "#"*50)
    print("Manual Rating Query")
    print("#"*50)
    for model_name in model_name:
        result, elapsed_time = print_result_for_model(
            model_name=model_name,
            query=MANUAL_RATING_QUERY,
            top_k=top_k
        )
        if not result:
            print("NO RESULTS FOUND")
            continue
        print(f"Elapsed Time for {model_name}: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    general_comparision()
    manual_comparision()


# =================================================================================
# Output
# =================================================================================

# ##################################################
# MODEL: all-MiniLM-L6-v2
# ##################################################
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# MODEL: all-MiniLM-L6-v2
# QUERY: construction toys
# TIME: 6.4946 seconds
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# Top Results:
# --------------------------------------------------
# 1. Geometry Shape Sorter Toy
#    Score: 0.4708
#    Description: A classic wooden toy that helps children learn about different shapes and develop fine motor skills.
#    Category: Early Learning
#    Brand: ShapeUp
#    Price: 18.75
#    Quantity: 95

# 2. Mini Robot Construction Kit
#    Score: 0.4696
#    Description: Build your own small, functional robot with this engaging construction kit, featuring easy-to-follow instructions.
#    Category: building blocks
#    Brand: RoboBuild
#    Price: 29.5
#    Quantity: 120

# 3. Lego Castle
#    Score: 0.4670
#    Description: brick set for building a castle with towers and walls for kids
#    Category: building blocks
#    Brand: LEGO
#    Price: 499.0
#    Quantity: 8

# 4. Kids Soccer Goal Set
#    Score: 0.4580
#    Description: A portable soccer goal set, easy to assemble and perfect for practicing soccer skills in the yard.
#    Category: outdoor toys
#    Brand: Sporty Kids
#    Price: 35.0
#    Quantity: 70

# 5. Sand Play Set with Molds
#    Score: 0.4563
#    Description: A complete sand play set including buckets, shovels, and various molds for creative sandcastles.
#    Category: outdoor toys
#    Brand: Beach Builders
#    Price: 16.0
#    Quantity: 130


# == == == == == == == == == == == == == == == == == == == == == == == == ==
# MODEL: all-MiniLM-L6-v2
# QUERY: gifts for toddlers
# TIME: 0.5178 seconds
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# Top Results:
# --------------------------------------------------
# 1. Backpack & School Accessories for Dolls
#    Score: 0.4935
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category: Dolls & Accessories
#    Brand: DollieDreams
#    Price: 15.25
#    Quantity: 110

# 2. Mini Animal Plush Assortment
#    Score: 0.4768
#    Description: A collection of small, cute plush animals, perfect for party favors or collecting.
#    Category: plush toys
#    Brand: Tiny Treasures
#    Price: 9.99
#    Quantity: 200

# 3. Alphabet Learning Puzzle
#    Score: 0.4707
#    Description: A wooden peg puzzle designed to help toddlers learn letters and improve fine motor skills.
#    Category: puzzles
#    Brand: SmartStart Toys
#    Price: 12.25
#    Quantity: 150

# 4. Kids Soccer Goal Set
#    Score: 0.4578
#    Description: A portable soccer goal set, easy to assemble and perfect for practicing soccer skills in the yard.
#    Category: outdoor toys
#    Brand: Sporty Kids
#    Price: 35.0
#    Quantity: 70

# 5. Kids First Microscope Kit
#    Score: 0.4465
#    Description: An easy-to-use microscope designed for children to explore the micro-world, includes slides and tools.
#    Category: educational toys
#    Brand: Science Explorers
#    Price: 39.99
#    Quantity: 70


# == == == == == == == == == == == == == == == == == == == == == == == == ==
# MODEL: all-MiniLM-L6-v2
# QUERY: pretend play toys
# TIME: 0.5558 seconds
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# Top Results:
# --------------------------------------------------
# 1. Teacher Role Play Set
#    Score: 0.5873
#    Description: A fun costume and accessory set for kids to pretend play as a teacher, complete with glasses, pointer, and chalk.
#    Category: Role Play
#    Brand: PretendPro
#    Price: 28.0
#    Quantity: 65

# 2. Play-Doh School Days Set
#    Score: 0.4818
#    Description: A themed Play-Doh set with molds and tools to create school-related objects like pencils, books, and apples.
#    Category: Creative Play
#    Brand: DohFun
#    Price: 16.99
#    Quantity: 115

# 3. Lunchbox & Thermos Pretend Play Set
#    Score: 0.4449
#    Description: A realistic play set featuring a lunchbox, thermos, and pretend food items for imaginative mealtime scenarios.
#    Category: Role Play
#    Brand: KitchenKids
#    Price: 13.5
#    Quantity: 125

# 4. Sand Play Set with Molds
#    Score: 0.4253
#    Description: A complete sand play set including buckets, shovels, and various molds for creative sandcastles.
#    Category: outdoor toys
#    Brand: Beach Builders
#    Price: 16.0
#    Quantity: 130

# 5. Doctor Play Doll Set
#    Score: 0.4177
#    Description: An articulated doll dressed as a doctor, complete with medical tools for role-playing and learning.
#    Category: dolls
#    Brand: Career Dolls
#    Price: 24.5
#    Quantity: 110


# == == == == == == == == == == == == == == == == == == == == == == == == ==
# MODEL: all-MiniLM-L6-v2
# QUERY: science and learning toys
# TIME: 0.5539 seconds
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# Top Results:
# --------------------------------------------------
# 1. Educational Robot Kit
#    Score: 0.5905
#    Description: A fun and interactive robot kit designed to introduce kids to basic coding and STEM principles, perfect for back-to-school learning.
#    Category: Educational Toys
#    Brand: RoboKids
#    Price: 49.99
#    Quantity: 75

# 2. Kids' Learning Tablet Toy
#    Score      : 0.5537
#    Description: An interactive electronic tablet with educational games and activities for letters, numbers, and shapes.
#    Category   : Electronic Learning
#    Brand      : SmartStart
#    Price      : 32.0
#    Quantity   : 70

# 3. Science Experiment Lab Kit
#    Score      : 0.5438
#    Description: An exciting kit with safe experiments for kids to explore chemistry and physics concepts at home.
#    Category   : Science Kits
#    Brand      : LabWonders
#    Price      : 39.0
#    Quantity   : 60

# 4. Geometry Shape Sorter Toy
#    Score      : 0.5408
#    Description: A classic wooden toy that helps children learn about different shapes and develop fine motor skills.
#    Category   : Early Learning
#    Brand      : ShapeUp
#    Price      : 18.75
#    Quantity   : 95

# 5. Kids First Microscope Kit
#    Score      : 0.5295
#    Description: An easy-to-use microscope designed for children to explore the micro-world, includes slides and tools.
#    Category   : educational toys
#    Brand      : Science Explorers
#    Price      : 39.99
#    Quantity   : 70


# ==================================================
# MODEL: all-MiniLM-L6-v2
# QUERY: soft cuddly toys
# TIME : 0.5704 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Baby Cuddle Doll
#    Score      : 0.6768
#    Description: A soft-bodied baby doll perfect for cuddling and nurturing play, comes with a pacifier and blanket.
#    Category   : dolls
#    Brand      : Sweet Dreams Babies
#    Price      : 15.75
#    Quantity   : 130

# 2. Giant Plush Teddy Bear
#    Score      : 0.6066
#    Description: An extra-large, super soft teddy bear, perfect for cuddling and a wonderful companion for children.
#    Category   : Plush Toys
#    Brand      : Cuddle Buddies
#    Price      : 35.99
#    Quantity   : 40

# 3. Snuggle Buddy Teddy Bear
#    Score      : 0.6034
#    Description: Super soft and cuddly teddy bear, perfect for hugs and comfort.
#    Category   : Plush Toys
#    Brand      : CuddleCo
#    Price      : 15.5
#    Quantity   : 75

# 4. Puppy Dog Plush
#    Score      : 0.5862
#    Description: An adorable plush puppy dog with floppy ears and a wagging tail, realistic and huggable.
#    Category   : plush toys
#    Brand      : Pet Pals
#    Price      : 18.0
#    Quantity   : 120

# 5. Giant Teddy Bear
#    Score      : 0.5728
#    Description: An extra-large, super soft teddy bear, perfect for big hugs and comforting companionship.
#    Category   : plush toys
#    Brand      : Cuddle Buddies
#    Price      : 45.0
#    Quantity   : 65

# Total Time for all-MiniLM-L6-v2: 8.6925 seconds

# ##################################################
# MODEL: all-mpnet-base-v2
# ##################################################
# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: construction toys
# TIME : 49.8138 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Mini Robot Construction Kit
#    Score      : 0.6087
#    Description: Build your own small, functional robot with this engaging construction kit, featuring easy-to-follow instructions.
#    Category   : building blocks
#    Brand      : RoboBuild
#    Price      : 29.5
#    Quantity   : 120

# 2. Play-Doh School Days Set
#    Score      : 0.5336
#    Description: A themed Play-Doh set with molds and tools to create school-related objects like pencils, books, and apples.
#    Category   : Creative Play
#    Brand      : DohFun
#    Price      : 16.99
#    Quantity   : 115

# 3. School Bus Building Blocks Set
#    Score      : 0.5230
#    Description: A large building block set allowing children to construct their own school bus and other school-themed structures.
#    Category   : Building Blocks
#    Brand      : BrickMaster
#    Price      : 35.75
#    Quantity   : 90

# 4. Educational Robot Kit
#    Score      : 0.4986
#    Description: A fun and interactive robot kit designed to introduce kids to basic coding and STEM principles, perfect for back-to-school learning.
#    Category   : Educational Toys
#    Brand      : RoboKids
#    Price      : 49.99
#    Quantity   : 75

# 5. Deluxe City Building Blocks Set
#    Score      : 0.4981
#    Description: A large set of colorful interlocking blocks for creative construction, perfect for developing motor skills and imagination.
#    Category   : building blocks
#    Brand      : BlockMaster
#    Price      : 49.99
#    Quantity   : 75


# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: gifts for toddlers
# TIME : 3.1088 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Kids' Learning Tablet Toy
#    Score      : 0.4435
#    Description: An interactive electronic tablet with educational games and activities for letters, numbers, and shapes.
#    Category   : Electronic Learning
#    Brand      : SmartStart
#    Price      : 32.0
#    Quantity   : 70

# 2. Alphabet Learning Puzzle
#    Score      : 0.4324
#    Description: A wooden peg puzzle designed to help toddlers learn letters and improve fine motor skills.
#    Category   : puzzles
#    Brand      : SmartStart Toys
#    Price      : 12.25
#    Quantity   : 150

# 3. Kids First Microscope Kit
#    Score      : 0.4260
#    Description: An easy-to-use microscope designed for children to explore the micro-world, includes slides and tools.
#    Category   : educational toys
#    Brand      : Science Explorers
#    Price      : 39.99
#    Quantity   : 70

# 4. Mini Animal Plush Assortment
#    Score      : 0.4192
#    Description: A collection of small, cute plush animals, perfect for party favors or collecting.
#    Category   : plush toys
#    Brand      : Tiny Treasures
#    Price      : 9.99
#    Quantity   : 200

# 5. Backpack & School Accessories for Dolls
#    Score      : 0.4050
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category   : Dolls & Accessories
#    Brand      : DollieDreams
#    Price      : 15.25
#    Quantity   : 110


# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: pretend play toys
# TIME : 3.3789 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Play-Doh School Days Set
#    Score      : 0.6218
#    Description: A themed Play-Doh set with molds and tools to create school-related objects like pencils, books, and apples.
#    Category   : Creative Play
#    Brand      : DohFun
#    Price      : 16.99
#    Quantity   : 115

# 2. Teacher Role Play Set
#    Score      : 0.5782
#    Description: A fun costume and accessory set for kids to pretend play as a teacher, complete with glasses, pointer, and chalk.
#    Category   : Role Play
#    Brand      : PretendPro
#    Price      : 28.0
#    Quantity   : 65

# 3. Backpack & School Accessories for Dolls
#    Score      : 0.5737
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category   : Dolls & Accessories
#    Brand      : DollieDreams
#    Price      : 15.25
#    Quantity   : 110

# 4. Doctor Play Doll Set
#    Score      : 0.5435
#    Description: An articulated doll dressed as a doctor, complete with medical tools for role-playing and learning.
#    Category   : dolls
#    Brand      : Career Dolls
#    Price      : 24.5
#    Quantity   : 110

# 5. Lunchbox & Thermos Pretend Play Set
#    Score      : 0.5394
#    Description: A realistic play set featuring a lunchbox, thermos, and pretend food items for imaginative mealtime scenarios.
#    Category   : Role Play
#    Brand      : KitchenKids
#    Price      : 13.5
#    Quantity   : 125


# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: science and learning toys
# TIME : 3.0360 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Educational Robot Kit
#    Score      : 0.6326
#    Description: A fun and interactive robot kit designed to introduce kids to basic coding and STEM principles, perfect for back-to-school learning.
#    Category   : Educational Toys
#    Brand      : RoboKids
#    Price      : 49.99
#    Quantity   : 75

# 2. Science Experiment Lab Kit
#    Score      : 0.6261
#    Description: An exciting kit with safe experiments for kids to explore chemistry and physics concepts at home.
#    Category   : Science Kits
#    Brand      : LabWonders
#    Price      : 39.0
#    Quantity   : 60

# 3. Kids' Learning Tablet Toy
#    Score      : 0.6214
#    Description: An interactive electronic tablet with educational games and activities for letters, numbers, and shapes.
#    Category   : Electronic Learning
#    Brand      : SmartStart
#    Price      : 32.0
#    Quantity   : 70

# 4. Kids' First Microscope Kit
#    Score      : 0.5826
#    Description: An easy-to-use microscope designed for young scientists to explore the microscopic world.
#    Category   : Science Kits
#    Brand      : MicroDiscovery
#    Price      : 29.95
#    Quantity   : 70

# 5. Kids First Microscope Kit
#    Score      : 0.5676
#    Description: An easy-to-use microscope designed for children to explore the micro-world, includes slides and tools.
#    Category   : educational toys
#    Brand      : Science Explorers
#    Price      : 39.99
#    Quantity   : 70


# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: soft cuddly toys
# TIME : 2.9562 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Baby Cuddle Doll
#    Score      : 0.7015
#    Description: A soft-bodied baby doll perfect for cuddling and nurturing play, comes with a pacifier and blanket.
#    Category   : dolls
#    Brand      : Sweet Dreams Babies
#    Price      : 15.75
#    Quantity   : 130

# 2. Snuggle Buddy Teddy Bear
#    Score      : 0.6119
#    Description: Super soft and cuddly teddy bear, perfect for hugs and comfort.
#    Category   : Plush Toys
#    Brand      : CuddleCo
#    Price      : 15.5
#    Quantity   : 75

# 3. Mini Animal Plush Assortment
#    Score      : 0.5654
#    Description: A collection of small, cute plush animals, perfect for party favors or collecting.
#    Category   : plush toys
#    Brand      : Tiny Treasures
#    Price      : 9.99
#    Quantity   : 200

# 4. Giant Plush Teddy Bear
#    Score      : 0.5555
#    Description: An extra-large, super soft teddy bear, perfect for cuddling and a wonderful companion for children.
#    Category   : Plush Toys
#    Brand      : Cuddle Buddies
#    Price      : 35.99
#    Quantity   : 40

# 5. Backpack & School Accessories for Dolls
#    Score      : 0.5008
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category   : Dolls & Accessories
#    Brand      : DollieDreams
#    Price      : 15.25
#    Quantity   : 110

# Total Time for all-mpnet-base-v2: 62.2937 seconds

# ##################################################
# Manual Rating Query
# ##################################################

# ==================================================
# MODEL: all-MiniLM-L6-v2
# QUERY: toys for 5-year-olds
# TIME : 0.6343 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Geometry Shape Sorter Toy
#    Score      : 0.5365
#    Description: A classic wooden toy that helps children learn about different shapes and develop fine motor skills.
#    Category   : Early Learning
#    Brand      : ShapeUp
#    Price      : 18.75
#    Quantity   : 95

# 2. Kids' Learning Tablet Toy
#    Score      : 0.5357
#    Description: An interactive electronic tablet with educational games and activities for letters, numbers, and shapes.
#    Category   : Electronic Learning
#    Brand      : SmartStart
#    Price      : 32.0
#    Quantity   : 70

# 3. Backpack & School Accessories for Dolls
#    Score      : 0.5091
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category   : Dolls & Accessories
#    Brand      : DollieDreams
#    Price      : 15.25
#    Quantity   : 110

# 4. Kids Soccer Goal Set
#    Score      : 0.5017
#    Description: A portable soccer goal set, easy to assemble and perfect for practicing soccer skills in the yard.
#    Category   : outdoor toys
#    Brand      : Sporty Kids
#    Price      : 35.0
#    Quantity   : 70

# 5. Kids First Microscope Kit
#    Score      : 0.5002
#    Description: An easy-to-use microscope designed for children to explore the micro-world, includes slides and tools.
#    Category   : educational toys
#    Brand      : Science Explorers
#    Price      : 39.99
#    Quantity   : 70

# Elapsed Time for all-MiniLM-L6-v2: 0.6343 seconds

# ==================================================
# MODEL: all-mpnet-base-v2
# QUERY: toys for 5-year-olds
# TIME : 2.9731 seconds
# ==================================================
# Top Results:
# --------------------------------------------------
# 1. Play-Doh School Days Set
#    Score      : 0.4717
#    Description: A themed Play-Doh set with molds and tools to create school-related objects like pencils, books, and apples.
#    Category   : Creative Play
#    Brand      : DohFun
#    Price      : 16.99
#    Quantity   : 115

# 2. Kids' Learning Tablet Toy
#    Score      : 0.4425
#    Description: An interactive electronic tablet with educational games and activities for letters, numbers, and shapes.
#    Category   : Electronic Learning
#    Brand      : SmartStart
#    Price      : 32.0
#    Quantity   : 70

# 3. Sand Play Set with Molds
#    Score      : 0.4365
#    Description: A complete sand play set including buckets, shovels, and various molds for creative sandcastles.
#    Category   : outdoor toys
#    Brand      : Beach Builders
#    Price      : 16.0
#    Quantity   : 130

# 4. Hula Hoop Assortment
#    Score      : 0.4302
#    Description: Colorful hula hoops in various sizes, promoting active play and coordination.
#    Category   : outdoor toys
#    Brand      : Hoop Stars
#    Price      : 7.99
#    Quantity   : 220

# 5. Backpack & School Accessories for Dolls
#    Score      : 0.4293
#    Description: A cute set of miniature school accessories including a backpack, books, and pretend lunch for 18-inch dolls.
#    Category   : Dolls & Accessories
#    Brand      : DollieDreams
#    Price      : 15.25
#    Quantity   : 110

# Elapsed Time for all-mpnet-base-v2: 2.9731 seconds
