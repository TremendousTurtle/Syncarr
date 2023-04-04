from flaskarr.extensions import db, ma
import datetime

# Sqlalchemy model that represents a release fetched by Sonarr or Radarr and downloaded by rTorrent which will be transferred from the remote server to the local server including local path, remote path, size, transferred size, status, Sonarr/Radarr ID, and rTorrent ID.
class Release(db.Model):
    __tablename__ = 'releases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    local_path = db.Column(db.String, nullable=False)
    remote_path = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    transferred_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    arr_id = db.Column(db.Integer, nullable=False)
    rtorrent_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    files = db.relationship('File', back_populates='release')

    def __repr__(self) -> str:
        return f'Release(id={self.id}, name={self.name}, local_path={self.local_path}, remote_path={self.remote_path}, size={self.size}, transferred_size={self.transferred_size}, status={self.status}, arr_id={self.arr_id}, rtorrent_id={self.rtorrent_id}, created_at={self.created_at}, updated_at={self.updated_at})'

    
# Model that represets files that are part of a release.
class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    transferred_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    release = db.relationship('Release', back_populates='files')

    def __repr__(self) -> str:
        return f'File(id={self.id}, release_id={self.release_id}, name={self.name}, size={self.size}, transferred_size={self.transferred_size}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at})'
    
# Marshmallow schema that represents a release.
class ReleaseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Release
        include_relationships = True
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    local_path = ma.auto_field()
    remote_path = ma.auto_field()
    size = ma.auto_field()
    transferred_size = ma.auto_field()
    status = ma.auto_field()
    arr_id = ma.auto_field()
    rtorrent_id = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    files = ma.Nested('FileSchema', many=True)

class FileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = File
        include_relationships = True
        load_instance = True

    id = ma.auto_field()
    release_id = ma.auto_field()
    name = ma.auto_field()
    size = ma.auto_field()
    transferred_size = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    release = ma.Nested('ReleaseSchema')