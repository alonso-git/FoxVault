from asyncpg.pool import PoolConnectionProxy


async def create_db(conn: PoolConnectionProxy):
    """
    Creates DB tables from scratch using direct SQL queries
    """

    query = """
    CREATE TABLE Accounts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        institution VARCHAR(50) NOT NULL,
        alias VARCHAR(100),
        type INT,
        balance NUMERIC(10, 2) DEFAULT 0.00
    );

    CREATE TABLE Transactions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        amount NUMERIC(10, 2) DEFAULT 0.00,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        origin_device VARCHAR(20) NOT NULL,
        description VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        account_id UUID REFERENCES Accounts(id) ON DELETE CASCADE
    );
    """

    await conn.execute(query)
    print("DB schema created")

async def clear_db(conn: PoolConnectionProxy):
    """
    WARNING: This function drops all tables and data
    """
    query = """
    DROP TABLE IF EXISTS Transactions CASCADE;
    DROP TABLE IF EXISTS Accounts CASCADE;
    """

    await conn.execute(query)
    print("DB empty")

async def reset_db(conn: PoolConnectionProxy):
    await clear_db(conn)
    await create_db(conn)

    print("DB reset (tables exist and are empty)")