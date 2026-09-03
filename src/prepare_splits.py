import os
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
INPUT_CSV = os.path.join(DATA_DIR, 'indian_fake_news_corpus.csv')
SPLITS_DIR = os.path.join(DATA_DIR, 'splits')

def create_reproducible_splits(test_size=0.10, val_size=0.10, random_state=42):
    """
    Creates stratified, reproducible Train / Validation / Test splits.
    Default: 80% Train, 10% Validation, 10% Test.
    """
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input corpus not found at {INPUT_CSV}")
        
    df = pd.read_csv(INPUT_CSV)
    os.makedirs(SPLITS_DIR, exist_ok=True)
    
    print(f"Loaded master corpus: {len(df)} samples")
    print(f"Class balance:\n{df['label'].value_counts()}")
    
    # First split: Train + Val vs Test (90% / 10%)
    train_val_df, test_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df['label'],
        random_state=random_state
    )
    
    # Second split: Train vs Val (from the 90%, take val_size/(1-test_size) = 0.1/0.9 = 11.11%)
    val_ratio_of_remaining = val_size / (1.0 - test_size)
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_ratio_of_remaining,
        stratify=train_val_df['label'],
        random_state=random_state
    )
    
    # Save splits
    train_df.to_csv(os.path.join(SPLITS_DIR, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(SPLITS_DIR, 'val.csv'), index=False)
    test_df.to_csv(os.path.join(SPLITS_DIR, 'test.csv'), index=False)
    
    print("\n" + "=" * 55)
    print("🎯 REPRODUCIBLE SPLITS GENERATED")
    print("=" * 55)
    print(f"  • Train set: {len(train_df)} rows ({len(train_df)/len(df)*100:.1f}%) -> data/splits/train.csv")
    print(f"  • Val set:   {len(val_df)} rows ({len(val_df)/len(df)*100:.1f}%) -> data/splits/val.csv")
    print(f"  • Test set:  {len(test_df)} rows ({len(test_df)/len(df)*100:.1f}%) -> data/splits/test.csv")
    print("=" * 55)

if __name__ == '__main__':
    create_reproducible_splits()
