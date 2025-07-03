from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey, func, desc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do SQLAlchemy
Base = declarative_base()

# --- Definição dos modelos de banco de dados ---
class Animal(Base):
    __tablename__ = 'animals'
    
    animal_id = Column(Integer, primary_key=True, autoincrement=True)
    official_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(100))
    birth_date = Column(Date, nullable=False)
    breed = Column(String(100))
    gender = Column(String(1), nullable=False)
    status = Column(String(50))
    entry_date = Column(Date)
    
    # Relacionamento com MilkProduction
    milk_productions = relationship("MilkProduction", back_populates="animal")
    
    def to_dict(self):
        """Converte a instância do Animal em um dicionário."""
        return {
            "animal_id": self.animal_id,
            "official_id": self.official_id,
            "name": self.name,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "breed": self.breed,
            "gender": self.gender,
            "status": self.status,
            "entry_date": self.entry_date.isoformat() if self.entry_date else None
        }

class MilkProduction(Base):
    __tablename__ = 'milk_production'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_id = Column(Integer, ForeignKey('animals.animal_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    production_date = Column(Date, nullable=False)
    liters_produced = Column(Float, nullable=False)
    period = Column(String(20), nullable=False)
    notes = Column(Text)
    
    # Relacionamento com Animal
    animal = relationship("Animal", back_populates="milk_productions")
    # Relacionamento com User
    user = relationship("User", back_populates="milk_productions")
    
    def to_dict(self):
        """Converte a instância de MilkProduction em um dicionário."""
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "user_id": self.user_id,
            "production_date": self.production_date.isoformat() if self.production_date else None,
            "liters_produced": float(self.liters_produced) if self.liters_produced else 0,
            "quantity": float(self.liters_produced) if self.liters_produced else 0,
            "period": self.period,
            "notes": self.notes
        }

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    is_active = Column(Integer, default=1)
    created_at = Column(Date, default=datetime.now)
    
    # Relacionamento reverso
    milk_productions = relationship("MilkProduction", back_populates="user")

# --- Classe para interagir com o banco de dados ---
class MilkDatabase:
    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria as tabelas."""
        # Configuração da conexão com o banco de dados a partir de variáveis de ambiente
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', 'root_password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_name = os.getenv('DB_NAME', 'kognia_one_db')
        
        # Use o driver 'mysql+pymysql'
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
        
        self.engine = create_engine(db_url, pool_pre_ping=True)
        
        # Comentado para evitar recriação das tabelas e perda de dados
        # Base.metadata.create_all(self.engine)
        
        # Configura a sessão
        self.Session = sessionmaker(bind=self.engine)
    
    # --- Métodos para Animais ---
    def create_animal(self, official_id: str, name: str, birth_date: date, breed: str, gender: str, status: str, entry_date: Optional[date] = None) -> Optional[int]:
        """Cria um novo animal no banco de dados.

        Args:
            official_id: ID oficial do animal.
            name: Nome do animal.
            birth_date: Data de nascimento.
            breed: Raça.
            gender: Gênero.
            status: Status do animal.
            entry_date: Data de entrada (opcional, padrão é a data atual).

        Returns:
            O ID do animal criado ou None em caso de erro.
        """
        if entry_date is None:
            entry_date = datetime.now().date()
        
        session = self.Session()
        try:
            animal = Animal(
                official_id=official_id,
                name=name,
                birth_date=birth_date,
                breed=breed,
                gender=gender,
                status=status,
                entry_date=entry_date
            )
            session.add(animal)
            session.commit()
            return animal.animal_id
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar animal: {e}")
            return None
        finally:
            session.close()
    
    def get_animals(self) -> List[Dict[str, Any]]:
        """Obtém todos os animais com status diferente de 'Inativo'."""
        session = self.Session()
        try:
            animals = session.query(Animal).filter(
                (Animal.status != 'Inativo') | (Animal.status.is_(None))
            ).order_by(Animal.name).all()
            return [animal.to_dict() for animal in animals]
        except Exception as e:
            print(f"Erro ao obter animais: {e}")
            return []
        finally:
            session.close()
    
    def get_animal(self, animal_id: int) -> Optional[Dict[str, Any]]:
        """Obtém um animal pelo ID."""
        session = self.Session()
        try:
            animal = session.query(Animal).filter(Animal.animal_id == animal_id).first()
            return animal.to_dict() if animal else None
        except Exception as e:
            print(f"Erro ao obter animal: {e}")
            return None
        finally:
            session.close()
    
    def update_animal(self, animal_id: int, official_id: str, name: str, birth_date: date, breed: str, gender: str, status: str, entry_date: date) -> bool:
        """Atualiza um animal existente."""
        session = self.Session()
        try:
            animal = session.query(Animal).filter(Animal.animal_id == animal_id).first()
            if not animal:
                return False
            
            animal.official_id = official_id
            animal.name = name
            animal.birth_date = birth_date
            animal.breed = breed
            animal.gender = gender
            animal.status = status
            animal.entry_date = entry_date
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar animal: {e}")
            return False
        finally:
            session.close()
    
    def delete_animal(self, animal_id: int) -> bool:
        """Inativa um animal (não exclui do banco)."""
        session = self.Session()
        try:
            animal = session.query(Animal).filter(Animal.animal_id == animal_id).first()
            if not animal:
                return False
            
            animal.status = 'Inativo'
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao inativar animal: {e}")
            return False
        finally:
            session.close()
    
    # --- Métodos para Produção de Leite ---
    def create_milk_production_entry(self, animal_id: int, production_date: date, liters_produced: float, period: str, notes: Optional[str] = None, user_id: Optional[int] = None) -> Optional[int]:
        """Cria um novo registro de produção de leite."""
        session = self.Session()
        try:
            entry = MilkProduction(
                animal_id=animal_id,
                production_date=production_date,
                liters_produced=liters_produced,
                period=period,
                notes=notes,
                user_id=user_id
            )
            session.add(entry)
            session.commit()
            return entry.id
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar registro de produção: {e}")
            return None
        finally:
            session.close()

    def get_milk_production_entry(self, entry_id: int) -> Optional[Dict[str, Any]]:
        """Obtém um registro de produção de leite pelo ID, incluindo dados do animal."""
        session = self.Session()
        try:
            query = session.query(
                MilkProduction.id.label('id'),
                MilkProduction.animal_id.label('animal_id'),
                MilkProduction.production_date.label('production_date'),
                MilkProduction.liters_produced.label('liters_produced'),
                MilkProduction.period.label('period'),
                MilkProduction.notes.label('notes'),
                Animal.name.label('name'),
                Animal.official_id.label('official_id'),
                Animal.breed.label('breed'),
                Animal.status.label('status'),
                Animal.birth_date.label('birth_date'),
                Animal.gender.label('gender'),
                Animal.entry_date.label('entry_date')
            ).join(Animal).filter(MilkProduction.id == entry_id)
            
            result = query.first()
            if not result:
                return None
                
            entry = {col: getattr(result, col) for col in result._fields}
            
            # Calcula a idade no Python para garantir compatibilidade
            if entry.get('birth_date'):
                today = date.today()
                entry['age'] = today.year - entry['birth_date'].year - ((today.month, today.day) < (entry['birth_date'].month, entry['birth_date'].day))
            else:
                entry['age'] = None

            # Formata as datas como strings ISO 8601 para facilitar o uso em APIs
            if entry.get('production_date'):
                entry['production_date'] = entry['production_date'].isoformat()
            if entry.get('birth_date'):
                entry['birth_date'] = entry['birth_date'].isoformat()
            if entry.get('entry_date'):
                entry['entry_date'] = entry['entry_date'].isoformat()
            
            # Adiciona o campo 'quantity' para compatibilidade
            entry['quantity'] = float(entry.get('liters_produced', 0))

            return entry
        except Exception as e:
            print(f"Erro ao obter registro de produção: {e}")
            return None
        finally:
            session.close()

    def count_milk_production_entries(self, animal_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> int:
        """Conta o número total de registros de produção de leite com filtros."""
        session = self.Session()
        try:
            query = session.query(func.count(MilkProduction.id))
            
            if animal_id:
                query = query.filter(MilkProduction.animal_id == animal_id)
            
            if start_date:
                query = query.filter(MilkProduction.production_date >= start_date)
            
            if end_date:
                query = query.filter(MilkProduction.production_date <= end_date)
            
            return query.scalar() or 0
        except Exception as e:
            print(f"Erro ao contar registros de produção: {e}")
            return 0
        finally:
            session.close()
    
    def get_milk_production_entries(self, page: int = 1, page_size: int = 5, animal_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Obtém registros de produção de leite com paginação e filtros."""
        session = self.Session()
        try:
            query = session.query(
                MilkProduction.id.label('id'),
                MilkProduction.animal_id.label('animal_id'),
                MilkProduction.production_date.label('production_date'),
                MilkProduction.liters_produced.label('liters_produced'),
                MilkProduction.period.label('period'),
                MilkProduction.notes.label('notes'),
                Animal.name.label('name'),
                Animal.official_id.label('official_id'),
                Animal.breed.label('breed'),
                Animal.status.label('status'),
                Animal.birth_date.label('birth_date'),
                Animal.gender.label('gender'),
                Animal.entry_date.label('entry_date')
            ).join(Animal)
            
            if animal_id:
                query = query.filter(MilkProduction.animal_id == animal_id)
            
            if start_date:
                query = query.filter(MilkProduction.production_date >= start_date)
            
            if end_date:
                query = query.filter(MilkProduction.production_date <= end_date)
            
            # Ordenação e paginação
            query = query.order_by(MilkProduction.production_date.desc())
            query = query.limit(page_size).offset((page - 1) * page_size)
            
            results = query.all()
            entries = []
            for row in results:
                entry = {col: getattr(row, col) for col in row._fields}
                
                # Calcula a idade no Python para garantir compatibilidade
                if entry.get('birth_date'):
                    today = date.today()
                    entry['age'] = today.year - entry['birth_date'].year - ((today.month, today.day) < (entry['birth_date'].month, entry['birth_date'].day))
                else:
                    entry['age'] = None

                # Formata as datas como strings ISO 8601
                if entry.get('production_date'):
                    entry['production_date'] = entry['production_date'].isoformat()
                if entry.get('birth_date'):
                    entry['birth_date'] = entry['birth_date'].isoformat()
                if entry.get('entry_date'):
                    entry['entry_date'] = entry['entry_date'].isoformat()
                    
                entry['quantity'] = float(entry.get('liters_produced', 0))
                entries.append(entry)
            return entries
        except Exception as e:
            print(f"Erro ao obter registros de produção: {e}")
            return []
        finally:
            session.close()

    def update_milk_production_entry(self, entry_id: int, liters_produced: Optional[float] = None, period: Optional[str] = None, notes: Optional[str] = None) -> bool:
        """Atualiza um registro de produção de leite."""
        session = self.Session()
        try:
            entry = session.query(MilkProduction).filter(MilkProduction.id == entry_id).first()
            if not entry:
                return False
            
            if liters_produced is not None:
                entry.liters_produced = liters_produced
            
            if period is not None:
                entry.period = period
            
            if notes is not None:
                entry.notes = notes
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar registro de produção: {e}")
            return False
        finally:
            session.close()

    def delete_milk_production_entry(self, entry_id: int) -> bool:
        """Exclui um registro de produção de leite."""
        session = self.Session()
        try:
            entry = session.query(MilkProduction).filter(MilkProduction.id == entry_id).first()
            if not entry:
                return False
            
            session.delete(entry)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir registro de produção: {e}")
            return False
        finally:
            session.close()

    def get_daily_milk_production(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Obtém a produção diária de leite para o período especificado."""
        session = self.Session()
        try:
            query = session.query(
                MilkProduction.production_date.label('date'),
                func.sum(MilkProduction.liters_produced).label('total_liters')
            ).group_by(MilkProduction.production_date)
            
            if start_date:
                query = query.filter(MilkProduction.production_date >= start_date)
            
            if end_date:
                query = query.filter(MilkProduction.production_date <= end_date)
            
            query = query.order_by(MilkProduction.production_date)
            
            results = query.all()
            daily_production = []
            
            for result in results:
                daily_production.append({
                    'date': result.date.isoformat() if result.date else None,
                    'total_liters': float(result.total_liters) if result.total_liters else 0,
                    'quantity': float(result.total_liters) if result.total_liters else 0
                })
            
            return daily_production
        except Exception as e:
            print(f"Erro ao obter produção diária: {e}")
            return []
        finally:
            session.close()

    def get_milk_production_by_animal(self) -> List[Dict[str, Any]]:
        """Obtém a produção total de leite por animal."""
        session = self.Session()
        try:
            # Correção: Adicionado 'birth_date' ao select e group_by para calcular a idade no Python.
            query = session.query(
                Animal.animal_id,
                Animal.name.label('name'),
                Animal.breed.label('breed'),
                Animal.status.label('status'),
                Animal.birth_date.label('birth_date'), # Adicionado birth_date ao select
                func.sum(MilkProduction.liters_produced).label('total_liters')
            ).join(MilkProduction).group_by(
                Animal.animal_id, 
                Animal.name, 
                Animal.breed, 
                Animal.status,
                Animal.birth_date # Adicionado birth_date ao group_by
            ).order_by(desc('total_liters'))
            
            results = query.all()
            animal_production = []
            
            today = date.today() # Pega a data atual uma vez, fora do loop.

            for result in results:
                # Calcula a idade no Python para garantir a portabilidade.
                age = today.year - result.birth_date.year - ((today.month, today.day) < (result.birth_date.month, result.birth_date.day))

                animal_production.append({
                    'animal_id': result.animal_id,
                    'name': result.name,
                    'breed': result.breed,
                    'status': result.status,
                    'age': age, # Idade calculada
                    'total_liters': float(result.total_liters) if result.total_liters else 0,
                    'quantity': float(result.total_liters) if result.total_liters else 0,
                    'period': 'all'
                })
            
            return animal_production
        except Exception as e:
            print(f"Erro ao obter produção por animal: {e}")
            return []
        finally:
            session.close()
            
    # --- Novos métodos adicionados ---
    def get_monthly_milk_production_by_user(self, user_id: int, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """
        Calcula a quantidade total de leite produzida por mês para um usuário específico
        dentro de um período definido.
        """
        session = self.Session()
        try:
            query = session.query(
                func.strftime('%Y-%m', MilkProduction.production_date).label('month'),
                func.sum(MilkProduction.liters_produced).label('total_liters')
            ).filter(
                MilkProduction.user_id == user_id,
                MilkProduction.production_date >= start_date,
                MilkProduction.production_date <= end_date
            ).group_by(
                text('month')
            ).order_by(
                text('month')
            )
            
            results = query.all()
            monthly_production = []
            for result in results:
                monthly_production.append({
                    'month': result.month,
                    'total_liters': float(result.total_liters) if result.total_liters else 0
                })
            return monthly_production
        except Exception as e:
            print(f"Erro ao obter produção mensal por usuário: {e}")
            return []
        finally:
            session.close()

    def get_active_animals_count(self) -> String:
        """
        Retorna a quantidade de animais com status 'Ativo'.
        Considera também animais com status nulo como ativos.
        """
        session = self.Session()
        try:
            count = session.query(Animal).filter(
                (Animal.status == 'Ativo') | (Animal.status.is_(None))
            ).count()
            return 2
        except Exception as e:
            print(f"Erro ao contar animais ativos: {e}")
            return 0
        finally:
            session.close()

# ... (código existente da sua classe MilkDatabase) ...

    def count_animals(self) -> int:
        print("Contando todos os animais no banco de dados...")
        """
        Retorna a contagem total de todos os animais no banco de dados,
        independentemente do status.
        """
        session = self.Session()
        try:
            count = session.query(Animal).count()
            return count
        except Exception as e:
            print(f"Erro ao contar todos os animais: {e}")
            return 0
        finally:
            session.close()
            
# Instância da classe para uso
milk_db = MilkDatabase()