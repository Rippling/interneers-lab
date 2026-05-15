# we will find precision, hit and recall
from week7.eval_dataset import SEARCH_TEST_CASES
from week7.semantic_search import semantic_search


# to make product name consistent
def normalize_name(text):
    return text.strip().lower()


# out of top k results returned how many were actually relavant
def precision_at_k(retrieved_names, relevant_names, k):
    top_k_names = retrieved_names[:k]

    if k == 0:
        return 0.0

    relevant_found = 0

    for name in top_k_names:
        if name in relevant_names:
            relevant_found += 1

    return relevant_found / k


# out of all relevant products that should have been found, how many did we retrieve in top k
def recall_at_k(retrieved_names, relevant_names, k):
    if not relevant_names:
        return 0.0

    top_k_names = retrieved_names[:k]
    relevant_found = 0

    for name in top_k_names:
        if name in relevant_names:
            relevant_found += 1

    return relevant_found / len(relevant_names)


# did at least one relevant item appear in k
def hit_at_k(retrieved_names, relevant_names, k):
    top_k_names = retrieved_names[:k]

    for name in top_k_names:
        if name in relevant_names:
            return 1.0

    return 0.0


# total irrelevant found/ actual irrelevant
def fallout_at_k(retrieved_names, irrelevant_names, k):
    if not irrelevant_names:
        return 0.0

    top_k_names = retrieved_names[:k]
    irrelevant_found = 0

    for name in top_k_names:
        if name in irrelevant_names:
            irrelevant_found += 1

    return irrelevant_found / len(irrelevant_names)


def evaluate_semantic_search(top_k=5, model_name="all-MiniLM-L6-v2"):
    all_precisions = []
    all_recalls = []
    all_hits = []
    all_fallouts = []

    print("\nSemantic Search Evaluation")
    print("=" * 50)

    # case_number = 1,2,3,...
    # test_case = dict containing query + relevant + irrelevant products
    for case_number, test_case in enumerate(SEARCH_TEST_CASES, start=1):
        query = test_case["query"]

        relevant_products = set()
        for name in test_case["relevant_products"]:
            relevant_products.add(normalize_name(name))

        irrelevant_products = set()
        for name in test_case["irrelevant_products"]:
            irrelevant_products.add(normalize_name(name))

        results = semantic_search(
            query=query,
            top_k=top_k,
            model_name=model_name
        )

        retrieved_names = []
        for item in results:
            retrieved_names.append(normalize_name(item["name"]))

        p_at_k = precision_at_k(retrieved_names, relevant_products, top_k)
        r_at_k = recall_at_k(retrieved_names, relevant_products, top_k)
        h_at_k = hit_at_k(retrieved_names, relevant_products, top_k)
        f_at_k = fallout_at_k(retrieved_names, irrelevant_products, top_k)

        all_precisions.append(p_at_k)
        all_recalls.append(r_at_k)
        all_hits.append(h_at_k)
        all_fallouts.append(f_at_k)

        print(f"\nTest Case {case_number}")
        print("-" * 50)
        print(f"Query              : {query}")
        print(f"Relevant Products  : {sorted(relevant_products)}")
        print(f"Irrelevant Products: {sorted(irrelevant_products)}")
        print("Top Results        :")

        if not results:
            print("  No results found.")
        else:
            for rank, result in enumerate(results, start=1):
                print(
                    f"  {rank}. {result['name']} "
                    f"(score={result['semantic_score']:.4f}, category={result['category']})"
                )

        print(f"Precision: {p_at_k:.4f}")
        print(f"Recall   : {r_at_k:.4f}")
        print(f"Hit      : {h_at_k:.4f}")
        print(f"Fallout      : {f_at_k:.4f}")

    avg_precision = 0.0
    avg_recall = 0.0
    avg_hit = 0.0
    avg_fallout = 0.0

    if all_precisions:
        avg_precision = sum(all_precisions) / len(all_precisions)

    if all_recalls:
        avg_recall = sum(all_recalls) / len(all_recalls)

    if all_hits:
        avg_hit = sum(all_hits) / len(all_hits)

    if all_fallouts:
        avg_fallout = sum(all_fallouts) / len(all_fallouts)

    print("\nOverall Summary")
    print("=" * 50)
    print(f"Average Precision: {avg_precision:.4f}")
    print(f"Average Recall   : {avg_recall:.4f}")
    print(f"Average Hit      : {avg_hit:.4f}")
    print(f"Average Fallout  : {avg_fallout:.4f}")


if __name__ == "__main__":
    evaluate_semantic_search(top_k=5, model_name="all-MiniLM-L6-v2")


# ===========
# OUTPUT
# ===========


# Semantic Search Evaluation
# == == == == == == == == == == == == == == == == == == == == == == == == ==
# Test Case 1
# --------------------------------------------------
# Query: construction toys
# Relevant Products: ['deluxe city building blocks set', 'interlocking gear system', 'magnetic tile creativity set', 'mini robot construction kit', 'wooden farm animal blocks']
# Irrelevant Products: ['classic family board game', 'giant teddy bear', 'princess royal doll', 'superhero action figure']
# Top Results:
#   1. Geometry Shape Sorter Toy(score=0.4708, category=Early Learning)
#   2. Mini Robot Construction Kit(score=0.4696, category=building blocks)
#   3. Lego Castle(score=0.4670, category=building blocks)
#   4. Kids Soccer Goal Set(score=0.4580, category=outdoor toys)
#   5. Sand Play Set with Molds(score=0.4563, category=outdoor toys)
# Precision: 0.2000
# Recall: 0.2000
# Hit: 1.0000
# Fallout: 0.0000

# Test Case 2
# --------------------------------------------------
# Query: gifts for toddlers
# Relevant Products: ['alphabet learning puzzle', 'baby cuddle doll', 'mini animal plush assortment', 'puppy dog plush', 'wooden farm animal blocks']
# Irrelevant Products: ['flying drone with camera', 'galactic warrior action figure', 'high-speed rc race car', 'mystery detective game']
# Top Results:
#   1. Backpack & School Accessories for Dolls(score=0.4935, category=Dolls & Accessories)
#   2. Mini Animal Plush Assortment(score=0.4768, category=plush toys)
#   3. Alphabet Learning Puzzle(score=0.4707, category=puzzles)
#   4. Kids Soccer Goal Set(score=0.4578, category=outdoor toys)
#   5. Kids First Microscope Kit(score=0.4465, category=educational toys)
# Precision: 0.4000
# Recall: 0.4000
# Hit: 1.0000
# Fallout: 0.0000

# Test Case 3
# --------------------------------------------------
# Query: pretend play toys
# Relevant Products: ['baby cuddle doll', 'doctor play doll set', 'fantasy fairy doll', 'galactic warrior action figure', 'ninja warrior figure', 'princess royal doll', 'space explorer figure', 'starlight princess doll', 'superhero action figure']
# Irrelevant Products: ['animal kingdom puzzle (1000 pieces)', 'classic family board game', 'deluxe city building blocks set', 'kids first microscope kit']
# Top Results:
#   1. Teacher Role Play Set(score=0.5873, category=Role Play)
#   2. Play-Doh School Days Set(score=0.4818, category=Creative Play)
#   3. Lunchbox & Thermos Pretend Play Set(score=0.4449, category=Role Play)
#   4. Sand Play Set with Molds(score=0.4253, category=outdoor toys)
#   5. Doctor Play Doll Set(score=0.4177, category=dolls)
# Precision: 0.2000
# Recall: 0.1111
# Hit: 1.0000
# Fallout: 0.0000

# Test Case 4
# --------------------------------------------------
# Query: science and learning toys
# Relevant Products: ['chemistry lab set', 'coding robot for kids', 'human anatomy model kit', 'interactive globe with pen', 'kids first microscope kit']
# Irrelevant Products: ['giant teddy bear', 'princess royal doll', 'superhero action figure', 'water blaster super soaker']
# Top Results:
#   1. Educational Robot Kit(score=0.5905, category=Educational Toys)
#   2. Kids' Learning Tablet Toy (score=0.5537, category=Electronic Learning)
#   3. Science Experiment Lab Kit (score=0.5438, category=Science Kits)
#   4. Geometry Shape Sorter Toy (score=0.5408, category=Early Learning)
#   5. Kids First Microscope Kit (score=0.5295, category=educational toys)
# Precision: 0.2000
# Recall   : 0.2000
# Hit      : 1.0000
# Fallout      : 0.0000

# Test Case 5
# --------------------------------------------------
# Query              : soft cuddly toys
# Relevant Products  : ['dinosaur stuffed animal', 'giant plush teddy bear', 'giant teddy bear', 'mini animal plush assortment', 'puppy dog plush', 'unicorn plush toy']
# Irrelevant Products: ['chemistry lab set', 'mini robot construction kit', 'mystery detective game', 'remote control helicopter']
# Top Results        :
#   1. Baby Cuddle Doll (score=0.6768, category=dolls)
#   2. Giant Plush Teddy Bear (score=0.6066, category=Plush Toys)
#   3. Snuggle Buddy Teddy Bear (score=0.6034, category=Plush Toys)
#   4. Puppy Dog Plush (score=0.5862, category=plush toys)
#   5. Giant Teddy Bear (score=0.5728, category=plush toys)
# Precision: 0.6000
# Recall   : 0.5000
# Hit      : 1.0000
# Fallout      : 0.0000

# Test Case 6
# --------------------------------------------------
# Query              : remote control vehicles and flying toys
# Relevant Products  : ['flying drone with camera', 'high-speed rc race car', 'rc monster truck', 'remote control helicopter', 'robo-racer remote control car']
# Irrelevant Products: ['animal kingdom puzzle (1000 pieces)', 'giant teddy bear', 'outdoor ring toss game', 'princess royal doll']
# Top Results        :
#   1. Remote Control Helicopter (score=0.6012, category=remote control toys)
#   2. Flying Disc Set (score=0.5843, category=outdoor toys)
#   3. Flying Drone with Camera (score=0.5793, category=remote control toys)
#   4. Turbo Racer Remote Control Car (score=0.5728, category=Remote Control Toys)
#   5. Robo-Racer Remote Control Car (score=0.5656, category=Remote Control Toys)
# Precision: 0.6000
# Recall   : 0.6000
# Hit      : 1.0000
# Fallout      : 0.0000

# Test Case 7
# --------------------------------------------------
# Query              : outdoor play toys
# Relevant Products  : ['flying disc set', 'giant bubble wand kit', 'hula hoop assortment', 'jump rope with counter', 'kids outdoor swing set', 'kids soccer goal set', 'kite flying kit', 'outdoor ring toss game', 'sand play set with molds', 'water blaster super soaker']
# Irrelevant Products: ['3d eiffel tower puzzle', 'fashionista doll collection', 'interactive globe with pen', 'superhero action figure']
# Top Results        :
#   1. Kids Outdoor Swing Set (score=0.6322, category=outdoor toys)
#   2. Sand Play Set with Molds (score=0.6291, category=outdoor toys)
#   3. Kids Soccer Goal Set (score=0.5970, category=outdoor toys)
#   4. Outdoor Ring Toss Game (score=0.5838, category=outdoor toys)
#   5. Hula Hoop Assortment (score=0.5267, category=outdoor toys)
# Precision: 1.0000
# Recall   : 0.5000
# Hit      : 1.0000
# Fallout      : 0.0000

# Overall Summary
# ==================================================
# Average Precision: 0.4571
# Average Recall   : 0.3587
# Average Hit      : 1.0000
# Average Fallout  : 0.0000
